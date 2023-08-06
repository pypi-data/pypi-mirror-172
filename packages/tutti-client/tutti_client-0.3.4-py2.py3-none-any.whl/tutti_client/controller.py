import inspect
import hashlib
from collections import namedtuple
from typing import Optional

from .error import TuttiServerError

class Controller:
    def __init__(self, duct):
        self._duct = duct
        self._access_token = None
        self._register_send_call()

    async def _send(self, eid, data):
        rid = self._duct.next_rid()
        return await self._duct.send(rid, eid, data)

    async def _called(self, eid, data):
        ret = await self._duct.call(eid, data)
        if ret['success']:
            return ret['content']
        else:
            raise TuttiServerError(ret)

    def _call_or_send(self, eid, data, called = True):
        data['access_token'] = self._access_token
        f = self._called if called else self._send
        return f(eid, data)

    def _curried(self, method_name, called):
        def f(**kwargs):
            return getattr(self, method_name)(**kwargs, called=called)
        return f

    def _register_send_call(self):
        methods = [name for (name,f) in inspect.getmembers(self, predicate=inspect.ismethod) if not name.startswith('_')]
        for name in methods:
            getattr(self.__class__, name).send = self._curried(name, called=False)
            getattr(self.__class__, name).call = self._curried(name, called=True)

class ResourceController(Controller):
    """Controller methods to make requests relevant to Tutti.works' essential resources.

    An instance of this class is bound to TuttiClient object, which can be accessed from ``TuttiClient.resource``.
    For instance, methods can be executed in the format of ``TuttiClient.resource.<method_name>(<args>)``.
    See :ref:`Communication with Server <communication>` for further details.
    """
    def __init__(self, duct):
        super().__init__(duct)

    async def get_web_service_descriptor(self, called = True):
        """Requests a set of parameters that needs to be shared with backend.
        """
        return await self._call_or_send(self._duct.EVENT['SYSTEM_GET_WSD'], {}, called = called)

    async def sign_up(self, user_name: str, password_hash: Optional[str] = None, privilege_ids: list = [], called = True, **kwargs):
        """Signs up for a new user account.

        Args:
            user_name (:obj:`str`): User name.
            password_hash (:obj:`str`, optional): MD5-hashed password.
        """
        if 'password' in kwargs:
            password_hash = hashlib.md5(kwargs['password'].encode()).hexdigest()
        return await self._call_or_send(
                self._duct.EVENT['AUTHENTICATION_SIGN_UP'],
                {
                    'user_name': user_name,
                    'password_hash': password_hash,
                    'privilege_ids': privilege_ids
                },
                called = called
            )

    async def sign_in(self, user_name: str = None, password_hash: str = None, access_token: str = None, called = True, **kwargs):
        """Signs into Tutti.works server.

        This must be called before calling any other controller methods.
        A pair of `user_name` and `password_hash`, OR valid `access_token` must be specified as arguments.

        Args:
            user_name (:obj:`str`, optional): User name.
            password_hash (:obj:`str`, optional): MD5-hashed password.
            access_token (:obj:`str`, optional): Access token hash.
        """
        if 'password' in kwargs:
            password_hash = hashlib.md5(kwargs['password'].encode()).hexdigest()
        return await self._call_or_send(
                self._duct.EVENT['AUTHENTICATION_SIGN_IN'],
                {
                    'user_name': user_name,
                    'password_hash': password_hash,
                    'access_token': access_token
                },
                called = called
            )

    async def sign_out(self, called = True):
        return await self._call_or_send(
                self._duct.EVENT['AUTHENTICATION_SIGN_OUT'],
                {},
                called = called
            )

    async def get_user_ids(self, called = True):
        """Requests a list of available internal user IDs.
        """
        return await self._call_or_send(
                self._duct.EVENT['ACCOUNT_LIST_IDS'],
                {},
                called = called
            )

    async def delete_account(self, user_id: str, called = True):
        """Deletes an account.

        Args:
            user_id (:obj:`str`): Internal user ID.
        """
        return await self._call_or_send(
                self._duct.EVENT['ACCOUNT_DELETE'],
                { 'user_id': user_id },
                called = called
            )

    async def check_project_diff(self, project_name: str, called = True):
        """Checks whether a whole project has difference from the last build version.

        Args:
            project_name (:obj:`str`): Project name.
        """
        return await self._call_or_send(
                self._duct.EVENT['SYSTEM_BUILD_CHECK_PROJECT_DIFF'],
                { 'project_name': project_name },
                called = called
            )

    async def rebuild_project(self, project_name: str, called = True):
        """Rebuilds project for the newest version.

        Args:
            project_name (:obj:`str`): Project name.
        """
        return await self._call_or_send(
                self._duct.EVENT['SYSTEM_BUILD_REBUILD_PROJECT'],
                { 'project_name': project_name },
                called = called
            )

    async def list_projects(self, called = True):
        return await self._call_or_send(
                self._duct.EVENT['PROJECT_LIST'],
                {},
                called = called
            )

    async def create_project(self, project_name: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['PROJECT_ADD'],
                { 'project_name': project_name },
                called = called
            )

    async def delete_project(self, project_name: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['PROJECT_DELETE'],
                { 'project_name': project_name },
                called = called
            )

    async def get_project_scheme(self, project_name: str, cached: bool = True, called = True):
        """Requests a project scheme.

        Args:
            project_name (:obj:`str`): Project name.
            cached (:obj:`bool`): If True, scheme is loaded and returned from Tutti.works server memory without reflecting any changes made in the project's ``scheme.py``.
        """
        return await self._call_or_send(
                self._duct.EVENT['PROJECT_GET_SCHEME'],
                { 'project_name': project_name, cached: cached },
                called = called
            )

    async def create_template(self, project_name: str, template_name: str, preset_group_name: str, preset_name: str, called = True):
        """Creates a template for project.

        A list of available ``preset_group_name`` and ``preset_name`` can be found by calling list_template_presets.
        """
        return await self._call_or_send(
                self._duct.EVENT['PROJECT_ADD_TEMPLATE'],
                {
                    'project_name': project_name,
                    'template_name': template_name,
                    'preset_group_name': preset_group_name,
                    'preset_name': preset_name
                },
                called = called
            )

    async def delete_template(self, project_name: str, template_name: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['PROJECT_DELETE_TEMPLATE'],
                { 'project_name': project_name, 'template_name': template_name },
                called = called
            )

    async def list_templates(self, project_name: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['PROJECT_LIST_TEMPLATES'],
                { 'project_name': project_name },
                called = called
            )

    async def list_template_presets(self, project_name: str, called = True):
        """Requests a list of all available template presets.

        Note that the returned list is for the deployed version of Tutti.works server -- if a project specified in the argument was created in the older server version, some presets in the list is not available.

        Args:
            project_name (:obj:`str`): Project name.
        """
        return await self._call_or_send(
                self._duct.EVENT['PROJECT_LIST_TEMPLATE_PRESETS'],
                { 'project_name': project_name },
                called = called
            )

    async def list_responses_for_project(self, project_name: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_FOR_PROJECT'],
                { 'project_name': project_name },
                called = called
            )

    async def list_responses_for_template(self, project_name: str, template_name: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_FOR_TEMPLATE'],
                { 'project_name': project_name, 'template_name': template_name },
                called = called
            )

    async def list_responses_for_nanotask(self, nanotask_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_FOR_NANOTASK'],
                { 'nanotask_id': nanotask_id },
                called = called
            )

    async def list_responses_for_worker(self, worker_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_FOR_WORKER'],
                { 'worker_id': worker_id },
                called = called
            )

    async def list_responses_for_work_session(self, work_session_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_FOR_WORK_SESSION'],
                { 'work_session_id': work_session_id },
                called = called
            )

    async def watch_responses_for_project(self, project_name: str, last_watch_id: str = '-', exclusive: bool = True, called = True, **kwargs):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_WATCH_FOR_PROJECT'],
                { 'project_name': project_name, 'last_watch_id': last_watch_id, 'exclusive': exclusive },
                called = called
            )

    async def watch_responses_for_template(self, project_name: str, template_name: str, last_watch_id: str = '-', exclusive: bool = True, called = True, **kwargs):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_WATCH_FOR_TEMPLATE'],
                { 'project_name': project_name, 'template_name': template_name, 'last_watch_id': last_watch_id, 'exclusive': exclusive },
                called = called
            )

    async def watch_responses_for_nanotask(self, nanotask_id: str, last_watch_id: str = '-', exclusive: bool = True, called = True, **kwargs):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_WATCH_FOR_NANOTASK'],
                { 'nanotask_id': nanotask_id, 'last_watch_id': last_watch_id, 'exclusive': exclusive },
                called = called
            )

    async def watch_responses_for_worker(self, worker_id: str, last_watch_id: str = '-', exclusive: bool = True, called = True, **kwargs):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_WATCH_FOR_WORKER'],
                { 'worker_id': worker_id, 'last_watch_id': last_watch_id, 'exclusive': exclusive },
                called = called
            )

    async def watch_responses_for_automation_parameter_set(self, automation_parameter_set_id: str, last_watch_id: str = '-', exclusive: bool = True, called = True, **kwargs):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_WATCH_FOR_AUTOMATION_PARAMETER_SET'],
                { 'automation_parameter_set_id': automation_parameter_set_id, 'last_watch_id': last_watch_id, 'exclusive': exclusive },
                called = called
            )

    async def watch_responses_for_platform_parameter_set(self, platform_parameter_set_id: str, last_watch_id: str = '-', exclusive: bool = True, called = True, **kwargs):
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_WATCH_FOR_PLATFORM_PARAMETER_SET'],
                { 'platform_parameter_set_id': platform_parameter_set_id, 'last_watch_id': last_watch_id, 'exclusive': exclusive },
                called = called
            )

    async def list_projects_with_responses(self, called = True):
        """Requests a list of project names that collected at least one response record.
        """
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_PROJECTS'],
                {},
                called = called
            )

    async def list_templates_with_responses(self, project_name: str, called = True):
        """Requests a list of template names in a project that collected at least one response record.

        Args:
            project_name (:obj:`str`): Project name.
        """
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_TEMPLATES'],
                { 'project_name': project_name },
                called = called
            )

    async def list_nanotasks_with_responses(self, project_name: str, template_name: str, called = True):
        """Requests a list of nanotask IDs associated to a template that collected at least one response record.

        Args:
            project_name (:obj:`str`): Project name.
            template_name (:obj:`str`): Template name.
        """
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_NANOTASKS'],
                { 'project_name': project_name, 'template_name': template_name },
                called = called
            )

    async def list_workers_with_responses(self, project_name: str, called = True):
        """Requests a list of worker IDs that submitted at least one response record.

        Args:
            project_name (:obj:`str`): Project name.
            template_name (:obj:`str`): Template name.
        """
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_WORKERS'],
                { 'project_name': project_name },
                called = called
            )

    async def list_work_sessions_with_responses(self, project_name: str, called = True):
        """Requests a list of work session IDs of a project that collected at least one response record.

        Args:
            project_name (:obj:`str`): Project name.
        """
        return await self._call_or_send(
                self._duct.EVENT['RESPONSE_LIST_WORK_SESSIONS'],
                { 'project_name': project_name },
                called = called
            )

    async def list_workers_for_project(self, project_name: str, called = True):
        """Requests a list of worker IDs that contributed to the specified project.

        Args:
            project_name (:obj:`str`): Project name.
        """
        return await self._call_or_send(
                self._duct.EVENT['WORKER_LIST_FOR_PROJECT'],
                { 'project_name': project_name },
                called = called
            )

    async def list_nanotasks(self, project_name: str, template_name: str, called = True):
        """Requests a list of worker IDs that contributed to the specified project.

        Args:
            project_name (:obj:`str`): Project name.
        """
        return await self._call_or_send(
                self._duct.EVENT['NANOTASK_LIST'],
                { 'project_name': project_name, 'template_name': template_name },
                called = called
            )

    async def create_nanotasks(self, project_name: str, template_name: str, nanotasks: list, tag: Optional[str] = None, priority: Optional[int] = None, num_assignable: Optional[int] = True, called = True):
        """Creates one or more nanotasks.

        Args:
            project_name (:obj:`str`): Project name.
            template_name (:obj:`str`): Template name.
            nanotasks (:obj:`list`): Nanotask data, represented by a list of :obj:`dict` objects. As keys, each element `must` include: ``props`` (dict); and `can` have ``id`` (int), ``tag`` (str), ``priority`` (int), ``num_assignable`` (int), and ``reference_answers`` (dict).
            tag (:obj:`str`, optional): An arbitrary string field for tracking purposes; default value for nanotasks with no specified ``tag`` field.
            priority (:obj:`int`, optional): A value used for nanotask assignment priority -- 1 is the **most** important; default value for nanotasks with no specified ``priority`` field.
            num_assignable (:obj:`int`, optional): A maximum number of responses that can be collected for the nanotask; default value for nanotasks with no specified ``num_assignable`` field.
        """
        return await self._call_or_send(
                self._duct.EVENT['NANOTASK_ADD_MULTI_FOR_TEMPLATE'],
                {
                    'project_name': project_name,
                    'template_name': template_name,
                    'nanotasks': nanotasks,
                    'tag': tag,
                    'priority': priority,
                    'num_assignable': num_assignable
                },
                called = called
            )

    async def delete_nanotasks(self, nanotask_ids: list, called = True):
        """Deletes one or more nanotasks.

        Args:
            nanotask_ids (:obj:`list`): A list of internal nanotask IDs.
        """
        return await self._call_or_send(
                self._duct.EVENT['NANOTASK_DELETE'],
                { 'nanotask_ids': nanotask_ids },
                called = called
            )

    async def create_nanotask_group(self, name: str, nanotask_ids: list, project_name: str, template_name: str, called = True):
        """Creates a nanotask group for nanotasks.

        Args:
            nanotask_ids (:obj:`list`): A list of internal nanotask IDs.
            project_name (:obj:`str`): Project name.
            template_name (:obj:`str`): Template name.
        """
        return await self._call_or_send(
                self._duct.EVENT['NANOTASK_GROUP_ADD'],
                { 'name': name, 'nanotask_ids': nanotask_ids, 'project_name': project_name, 'template_name': template_name },
                called = called
            )

    async def list_nanotask_groups(self, project_name: str, template_name: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['NANOTASK_GROUP_LIST'],
                { 'project_name': project_name, 'template_name': template_name },
                called = called
            )

    async def get_nanotask_group(self, nanotask_group_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['NANOTASK_GROUP_GET'],
                { 'nanotask_group_id': nanotask_group_id },
                called = called
            )

    async def delete_nanotask_group(self, nanotask_group_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['NANOTASK_GROUP_DELETE'],
                { 'nanotask_group_id': nanotask_group_id },
                called = called
            )

    async def create_platform_parameter_set(self, name: str, platform: str, parameters: dict, called = True):
        return await self._call_or_send(
                self._duct.EVENT['PLATFORM_PARAMETER_SET_ADD'],
                { 'name': name, 'platform': platform, 'parameters': parameters },
                called = called
            )

    async def get_platform_parameter_set(self, platform_parameter_set_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['PLATFORM_PARAMETER_SET_GET'],
                { 'platform_parameter_set_id': platform_parameter_set_id },
                called = called
            )

    async def create_automation_parameter_set(self, name: str, platform_parameter_set_id: str, project_name: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['AUTOMATION_PARAMETER_SET_ADD'],
                { 'name': name, 'platform_parameter_set_id': platform_parameter_set_id, 'project_name': project_name },
                called = called
            )

    async def list_automation_parameter_sets(self, called = True):
        return await self._call_or_send(
                self._duct.EVENT['AUTOMATION_PARAMETER_SET_LIST'],
                {},
                called = called
            )


class MTurkController(Controller):
    """Controller methods to make requests relevant to Amazon MTurk operations.

    An instance of this class is bound to TuttiClient object, which can be accessed from ``TuttiClient.mturk``.
    For instance, methods can be executed in the format of ``TuttiClient.mturk.<method_name>(<args>)``.
    See :ref:`Communication with Server <communication>` for further details.
    """
    def __init__(self, duct):
        super().__init__(duct)

    async def get_active_credentials(self, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_GET_ACTIVE_CREDENTIALS'],
                {},
                called = called
            )
    async def set_active_credentials(self, credentials_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_SET_ACTIVE_CREDENTIALS'],
                { 'credentials_id': credentials_id },
                called = called
            )
    async def list_credentials(self, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_LIST_CREDENTIALS'],
                {},
                called = called
            )
    async def get_credentials(self, credentials_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_GET_CREDENTIALS'],
                { 'credentials_id': credentials_id },
                called = called
            )
    async def delete_credentials(self, credentials_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_DELETE_CREDENTIALS'],
                { 'credentials_id': credentials_id },
                called = called
            )
    async def rename_credentials(self, credentials_id: str, label: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_RENAME_CREDENTIALS'],
                { 'credentials_id': credentials_id, label: label },
                called = called
            )
    async def add_credentials(self, access_key_id: str, secret_access_key: str, label: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_ADD_CREDENTIALS'],
                { 'access_key_id': access_key_id, 'secret_access_key': secret_access_key, 'label': label },
                called = called
            )
    async def set_active_sandbox_mode(self, is_sandbox: bool, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_SET_ACTIVE_SANDBOX_MODE'],
                { 'is_sandbox': is_sandbox },
                called = called
            )
    async def exec_boto3(self, method: str, parameters: dict, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_EXEC_BOTO3'],
                { 'method': method, 'parameters': parameters },
                called = called
            )
    async def expire_hits(self, request_id: str, hit_ids: list[str], called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_HIT_EXPIRE'],
                { 'request_id': request_id, 'hit_ids': hit_ids },
                called = called
            )
    async def delete_hits(self, request_id: str, hit_ids: list[str], called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_HIT_DELETE'],
                { 'request_id': request_id, 'hit_ids': hit_ids },
                called = called
            )
    async def list_hits_for_tutti_hit_batch(self, batch_id: str, cached: bool, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_HIT_LIST_FOR_TUTTI_HIT_BATCH'],
                { 'batch_id': batch_id, 'cached': cached },
                called = called
            )
    async def list_tutti_hit_batches(self, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_TUTTI_HIT_BATCH_LIST'],
                {},
                called = called
            )
    async def list_tutti_hit_batches_with_hits(self, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_TUTTI_HIT_BATCH_LIST_WITH_HITS'],
                {},
                called = called
            )
    async def create_tutti_hit_batch(self, name: str, project_name: str, hit_type_params: dict, hit_params: dict, num_hits: int, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_TUTTI_HIT_BATCH_CREATE'],
                {
                    'name': name,
                    'project_name': project_name,
                    'hit_type_params': hit_type_params,
                    'hit_params': hit_params,
                    'num_hits': num_hits
                },
                called = called
            )
    async def add_hits_to_tutti_hit_batch(self, batch_id: str, hit_params: dict, num_hits: int, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_HIT_ADD_FOR_TUTTI_HIT_BATCH'],
                { 'batch_id': batch_id, 'hit_params': hit_params, 'num_hits': num_hits },
                called = called
            )
    async def delete_tutti_hit_batch(self, request_id: str, batch_id: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_TUTTI_HIT_BATCH_DELETE'],
                { 'request_id': request_id, 'batch_id': batch_id },
                    called = called
            )
    async def list_hit_types(self, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_HIT_TYPE_LIST'],
                {},
                called = called
            )
    async def list_qualification_types(self, query: str, only_user_defined: bool, cached: bool, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_QUALIFICATION_TYPE_LIST'],
                { 'query': query, 'only_user_defined': only_user_defined, 'cached': cached },
                called = called
            )
    async def create_qualification_type(self, name: str, description: str, auto_granted: bool, qualification_type_status: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_QUALIFICATION_TYPE_CREATE'],
                {
                    'name': name,
                    'description': description,
                    'auto_granted': auto_granted,
                    'qualification_type_status': qualification_type_status
                },
                called = called
            )
    async def delete_qualification_types(self, qualification_type_ids: list[str], called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_QUALIFICATION_TYPE_DELETE'],
                { 'qualification_type_ids': qualification_type_ids },
                called = called
            )
    async def list_workers(self, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_WORKER_LIST'],
                {},
                called = called
            )
    async def notify_workers(self, subject: str, message_text: str, worker_ids: list[str], called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_WORKER_NOTIFY'],
                { 'subject': subject, 'message_text': message_text, 'worker_ids': worker_ids },
                called = called
            )
    async def associate_qualifications_with_workers(self, qualification_type_id: str, worker_ids: list[str], integer_value: int, send_notification: bool, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_WORKER_ASSOCIATE_QUALIFICATIONS'],
                {
                    'qualification_type_id': qualification_type_id,
                    'worker_ids': worker_ids,
                    'integer_value': integer_value,
                    'send_notification': send_notification
                },
                called = called
            )
    async def list_assignments_for_tutti_hit_batch(self, batch_id: str, cached: bool, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_ASSIGNMENT_LIST_FOR_TUTTI_HIT_BATCH'],
                { 'batch_id': batch_id, 'cached': cached },
                called = called
            )
    async def approve_assignments(self, assignment_ids: list[str], requester_feedback: str, override_rejection: bool, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_ASSIGNMENT_APPROVE'],
                {
                    'assignment_ids': assignment_ids,
                    'requester_feedback': requester_feedback,
                    'override_rejection': override_rejection
                },
                called = called
            )
    async def reject_assignments(self, assignment_ids: list[str], requester_feedback: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_ASSIGNMENT_REJECT'],
                { 'assignment_ids': assignment_ids, 'requester_feedback': requester_feedback },
                called = called
            )
    async def send_bonus(self, worker_ids: list[str], bonus_amount: str, assignment_ids: list[str], reason: str, called = True):
        return await self._call_or_send(
                self._duct.EVENT['MARKETPLACE_MTURK_ASSIGNMENT_SEND_BONUS'],
                {
                    'worker_ids': worker_ids,
                    'bonus_amount': bonus_amount,
                    'assignment_ids': assignment_ids,
                    'reason': reason
                },
                called = called
            )
