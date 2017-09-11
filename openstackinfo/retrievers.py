import logging
from abc import ABCMeta, abstractmethod

import os
from concurrent.futures import ThreadPoolExecutor, FIRST_EXCEPTION, wait, Future
from enum import Enum, unique
from threading import Lock

import shade
from shade import OpenStackCloud
from typing import List, Dict, Callable

from openstackinfo.models import Credentials
from openstackinfo.schema import OPENSTACK_INSTANCES_JSON_KEY, OPENSTACK_VOLUMES_JSON_KEY, \
    OPENSTACK_NETWORKS_JSON_KEY, OPENSTACK_SECURITY_GROUPS_JSON_KEY, IndexedByTypeValidator, \
    OPENSTACK_IMAGES_JSON_KEY, OPENSTACK_KEYPAIRS_JSON_KEY, OPENSTACK_SUBNETS_JSON_KEY, OPENSTACK_ROUTERS_JSON_KEY, \
    RESOURCE_TYPE_MAPPINGS

_logger = logging.getLogger(__name__)


@unique
class EnvironmentVariable(Enum):
    """
    Environment variables that may be used by information retrievers to get settings.
    """
    OS_PASSWORD = "OS_PASSWORD"
    OS_USERNAME = "OS_USERNAME"
    OS_AUTH_URL = "OS_AUTH_URL"
    OS_TENANT_NAME = "OS_TENANT_NAME"


class InformationRetriever(metaclass=ABCMeta):
    """
    Gather of information from OpenStack about a tenant.
    """
    def get_openstack_info(self) -> Dict:
        """
        Gets information about OpenStack.
        :return: validated information about OpenStack
        """
        information = self._get_openstack_info()
        assert IndexedByTypeValidator().get_validity(information)
        return information

    @abstractmethod
    def _get_openstack_info(self) -> Dict:
        """
        Gets information about OpenStack without validation.
        :return: information about OpenStack
        """


class ShadeInformationRetriever(InformationRetriever):
    """
    Gets information about OpenStack tenant using the `shade` library.
    """
    MAX_SIMULTANEOUS_CONNECTIONS = len(RESOURCE_TYPE_MAPPINGS)
    _INFORMATION_REQUESTORS = {
        OPENSTACK_IMAGES_JSON_KEY: lambda retriever: retriever._connection.list_images(),
        OPENSTACK_INSTANCES_JSON_KEY: lambda retriever: retriever._connection.list_servers(detailed=True),
        OPENSTACK_KEYPAIRS_JSON_KEY: lambda retriever: retriever._connection.list_keypairs(),
        OPENSTACK_NETWORKS_JSON_KEY: lambda retriever: retriever._connection.list_networks(),
        OPENSTACK_SECURITY_GROUPS_JSON_KEY: lambda retriever: retriever._connection.list_security_groups(),
        OPENSTACK_SUBNETS_JSON_KEY: lambda retriever: retriever._connection.list_subnets(),
        OPENSTACK_ROUTERS_JSON_KEY: lambda retriever: retriever._connection.list_routers(),
        OPENSTACK_VOLUMES_JSON_KEY: lambda retriever: retriever._connection.list_volumes()
    }

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, credentials: Credentials):
        with self._connection_change_lock:
            self._credentials = credentials
            self._connection_cache = None

    @property
    def max_simultaneous_connections(self) -> int:
        return self._max_simultaneous_connections

    @property
    def _connection(self) -> OpenStackCloud:
        with self._connection_change_lock:
            if self._connection_cache is None:
                self._connection_cache = shade.openstack_cloud(
                    auth_url=self.credentials.auth_url,
                    project_name=self.credentials.tenant,
                    username=self.credentials.username,
                    password=self.credentials.password
                )
        return self._connection_cache

    def __init__(self, credentials: Credentials, max_simultaneous_connections=MAX_SIMULTANEOUS_CONNECTIONS):
        """
        Constructor.
        :param credentials: credentials used to access OpenStack API
        :param max_simultaneous_connections: the maximum number of simultaneous connections that should be sent to
        OpenStack at a time
        """
        self._connection_change_lock = Lock()
        self._credentials = None
        self._connection_cache = None
        self._max_simultaneous_connections = None
        self._max_simultaneous_connections = max_simultaneous_connections
        self._executor = ThreadPoolExecutor(max_workers=self.max_simultaneous_connections)
        self.credentials = credentials

    def _get_openstack_info(self) -> Dict:
        # Note: `os_client_config` parse all `OS_` variables... which would be fine if its parser didn't break when it
        # encounters certain values, e.g. https://bugs.launchpad.net/os-client-config/+bug/1635696. Hiding ext
        saved_env = {}
        for key in list(os.environ.keys()):
            if key.startswith("OS_") and key not in EnvironmentVariable.__members__:
                saved_env[key] = os.environ.pop(key)

        information: Dict[str, Dict] = {}

        def handle_request(name: str, requestor: Callable[[ShadeInformationRetriever], Dict]):
            information[name] = requestor(self)
            _logger.info(f"Loaded data for {name}")

        futures: List[Future] = []
        for name, requestor in ShadeInformationRetriever._INFORMATION_REQUESTORS.items():
            self._executor.submit(handle_request, name, requestor)
        wait(futures, return_when=FIRST_EXCEPTION)
        self._executor.shutdown()

        for future in futures:
            future.result()
        assert len(information) == len(ShadeInformationRetriever._INFORMATION_REQUESTORS)

        for key, value in saved_env.items():
            os.environ[key] = value

        return information


class DummyInformationRetriever(InformationRetriever):
    """
    Dummy implementation.
    """
    def __init__(self, information: Dict=None):
        self.information = information if information is not None else None

    def _get_openstack_info(self) -> Dict:
        return self.information
