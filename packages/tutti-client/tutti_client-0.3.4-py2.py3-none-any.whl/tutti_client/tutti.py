import asyncio
from typing import Optional
from ducts_client import Duct
from .controller import ResourceController, MTurkController
from .listener import ResourceEventListener, MTurkEventListener

class TuttiClient:
    """A facade class which communicates with Tutti server.

    Attributes:
        resource (ResourceManager): Member for Tutti.works' essential resources.
        mturk (MTurkManager): Member for operations relevant to Amazon Mechanical Turk.
        account_info (:obj:`dict`): Sign-in account information updated automatically on calling authentication methods.
    """
    def __init__(self):
        super()

        self._duct = Duct()
        self._opened = False

        self.account_info = {
            'user_name': None,
            'user_id': None,
            'access_token': None,
        }

    async def open(self, host: str, wsd_path: str = '/ducts/wsd'):
        """Opens connection with Tutti.works server.

        Args:
            host (:obj:`str`): Host name of Tutti.works server.
            wsd_path (:obj:`str`): Path from host root for obtaining DUCTS web service descriptor.
        """
        if not self._duct:
            self._duct = Duct()
        if wsd_path in host:
            host = host[:host.find(wsd_path)]
        await self._duct.open(host+wsd_path)

        self.resource = ResourceManager(self._duct)
        self.mturk = MTurkManager(self._duct)

        self.on_connection = self._duct.connection_listener

        wsd = await self.resource.get_web_service_descriptor.call()
        self.ENUM = wsd['enums']
        self.ERROR = wsd['enums']['errors']

        self.resource.on('sign_in', success=self._on_sign_in)
        self.resource.on('sign_out', success=self._on_sign_out)

        self._opened = True

    async def _on_sign_in(self, data):
        self._set_account_info(data)

    async def _on_sign_out(self):
        self._delete_account_info()

    async def reconnect(self):
        """Reconnects with Tutti.works server.
        """
        await self._duct.reconnect()

    def close(self):
        """Closes connection with Tutti.works server.
        """
        self._duct.close()

    def _set_account_info(self, data):
        self.account_info['user_name'] = data['user_name']
        self.account_info['user_id'] = data['user_id']
        self.account_info['access_token'] = data['access_token']
        self.resource._access_token = self.account_info['access_token']
        self.mturk._access_token = self.account_info['access_token']

    def _delete_account_info(self):
        self.account_info.user_name = None
        self.account_info.user_id = None
        self.account_info.access_token = None

class ResourceManager(ResourceController):
    """Controller methods and setter method of event listener for Tutti.works' essential resources.

    For the list of all available controller methods, see :ref:`ResourceController <resource_controller>`.

    Attributes:
        on (:obj:`function`): tutti_client.listener.ResourceEventListener.on
    """
    def __init__(self, duct):
        super().__init__(duct)
        self.on = ResourceEventListener(duct).on
        self._access_token = None

class MTurkManager(MTurkController):
    """Controller methods and setter method of event listener for Amazon MTurk related operations.

    For the list of all available controller methods, see :ref:`MTurkController <mturk_controller>`.

    Attributes:
        on (:obj:`function`): tutti_client.listener.MTurkEventListener.on
    """
    def __init__(self, duct):
        super().__init__(duct)
        self.on = MTurkEventListener(duct).on
        self._access_token = None
