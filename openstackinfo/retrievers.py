from abc import ABCMeta

import shade
from shade import OpenStackCloud
from typing import List, Dict

from openstackinfo.models import Credentials
from openstackinfo.schema import OPENSTACK_INSTANCES_JSON_KEY, OPENSTACK_VOLUMES_JSON_KEY, \
    OPENSTACK_NETWORKS_JSON_KEY, OPENSTACK_SECURITY_GROUPS_JSON_KEY, validate, INDEX_BY_TYPE_SCHEMA


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
        validate(information, INDEX_BY_TYPE_SCHEMA)
        return information

    def _get_openstack_info(self) -> Dict:
        """
        Gets information about OpenStack without validation.
        :return: information about OpenStack
        """


class ShadeInformationRetriever(InformationRetriever):
    """
    Gets information about OpenStack tenant using the `shade` library.
    """
    @property
    def _connection(self) -> OpenStackCloud:
        """
        Gets `shade` connection to OpenStack using the given credentials.
        :return: `shade` connection
        """
        if self._connection_cache is None:
            self._connection_cache = shade.openstack_cloud(
                auth_url=self.credentials.auth_url,
                project_name=self.credentials.tenant,
                username=self.credentials.username,
                password=self.credentials.password
            )
        return self._connection_cache

    def __init__(self, credentials: Credentials):
        """
        Constructor.
        :param credentials: credentials used to access OpenStack API
        """
        self.credentials = credentials
        self._connection_cache = None

    def _get_openstack_info(self) -> Dict:
        return {
            OPENSTACK_INSTANCES_JSON_KEY: self.get_server_info(),
            OPENSTACK_VOLUMES_JSON_KEY: self.get_volume_info(),
            OPENSTACK_NETWORKS_JSON_KEY: self.get_security_group_info(),
            OPENSTACK_SECURITY_GROUPS_JSON_KEY: self.get_network_info()
        }

    def get_network_info(self) -> List[Dict]:
        """
        Gets information about networks on OpenStack.
        :return: information about networks
        """
        return []

    def get_security_group_info(self) -> List[Dict]:
        """
        Gets information about security groups on OpenStack.
        :return: information about security groups
        """
        return []

    def get_volume_info(self) -> List[Dict]:
        """
        Gets information about volumes (attached and unattached) on OpenStack.
        :return: information about volumes
        """
        return []

    def get_server_info(self) -> List[Dict]:
        """
        Gets information about servers on OpenStack.
        :return: information about servers
        """
        return self._connection.list_servers(detailed=True)


class DummyInformationRetriever(InformationRetriever):
    """
    Dummy implementation.
    """
    def __init__(self, information: Dict=None):
        self.information = information if information else None

    def _get_openstack_info(self) -> Dict:
        return self.information
