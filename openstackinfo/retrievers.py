from abc import ABCMeta, abstractmethod

import shade
from shade import OpenStackCloud
from typing import List, Dict

from openstackinfo.models import Credentials
from openstackinfo.schema import OPENSTACK_INSTANCES_JSON_KEY, OPENSTACK_VOLUMES_JSON_KEY, \
    OPENSTACK_NETWORKS_JSON_KEY, OPENSTACK_SECURITY_GROUPS_JSON_KEY, IndexedByTypeValidator, OPENSTACK_IMAGES_JSON_KEY, \
    OPENSTACK_KEYPAIRS_JSON_KEY


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
            OPENSTACK_IMAGES_JSON_KEY: self.get_image_info(),
            OPENSTACK_INSTANCES_JSON_KEY: self.get_server_info(),
            OPENSTACK_KEYPAIRS_JSON_KEY: self.get_keypair_info(),
            OPENSTACK_NETWORKS_JSON_KEY: self.get_security_group_info(),
            OPENSTACK_SECURITY_GROUPS_JSON_KEY: self.get_network_info(),
            OPENSTACK_VOLUMES_JSON_KEY: self.get_volume_info()
        }

    def get_image_info(self) -> List[Dict]:
        """
        Gets information about image on OpenStack.
        :return: information about image
        """
        return self._connection.list_servers(detailed=True)

    def get_server_info(self) -> List[Dict]:
        """
        Gets information about servers on OpenStack.
        :return: information about servers
        """
        return self._connection.list_servers(detailed=True)

    def get_keypair_info(self) -> List[Dict]:
        """
        Gets information about keypairs on OpenStack.
        :return: information about image
        """
        return self._connection.list_keypairs()

    def get_network_info(self) -> List[Dict]:
        """
        Gets information about networks on OpenStack.
        :return: information about networks
        """
        return self._connection.list_networks()

    def get_security_group_info(self) -> List[Dict]:
        """
        Gets information about security groups on OpenStack.
        :return: information about security groups
        """
        return self._connection.list_security_groups()

    def get_volume_info(self) -> List[Dict]:
        """
        Gets information about volumes (attached and unattached) on OpenStack.
        :return: information about volumes
        """
        return self._connection.list_volumes()


class DummyInformationRetriever(InformationRetriever):
    """
    Dummy implementation.
    """
    def __init__(self, information: Dict=None):
        self.information = information if information is not None else None

    def _get_openstack_info(self) -> Dict:
        return self.information
