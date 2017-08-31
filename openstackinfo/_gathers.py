import shade
from Dict import Dict
from shade import OpenStackCloud
from typing import List, Dict

from openstackinfo.models import Credentials

ID_JSON_KEY = "id"
# NAME_JSON_KEY = "name"
TYPE_JSON_KEY = "type"

OPENSTACK_INSTANCES_JSON_KEY = "instances"
OPENSTACK_VOLUMES_JSON_KEY = "volumes"
OPENSTACK_NETWORKS_JSON_KEY = "networks"
OPENSTACK_SECURITY_GROUPS_JSON_KEY = "security_groups"

# NETWORK_SUBNET_IDS_JSON_KEY = "subnet_ids"
#
# VOLUME_ATTACHED_TO_JSON_KEY = "attached_to"
#
# SERVER_NETWORKS_JSON_KEY = "networks"
# SERVER_VOLUMES_JSON_KEY = "volumes_attached"
# SERVER_STATUS_JSON_KEY = "status"
# SERVER_CREATED_AT_JSON_KEY = "created"
# SERVER_UPDATED_AT_JSON_KEY = "updated"
# SERVER_SECURITY_GROUPS_JSON_KEY = "security_groups"
# SERVER_METADATA_JSON_KEY = "metadata"

_connection_cache = None


def _get_shade_connection(credentials: Credentials) -> OpenStackCloud:
    """
    Gets `shade` connection to OpenStack using the given credentials.

    The connection is cached and shared.
    :param credentials: credentials used to access OpenStack API
    :return: `shade` connection
    """
    global _connection_cache
    if _connection_cache is None:
        _connection_cache = shade.openstack_cloud(
            auth_url=credentials.auth_url,
            project_name=credentials.tenant,
            username=credentials.username,
            password=credentials.password
        )
    return _connection_cache


def get_network_info(credentials: Credentials) -> List[Dict]:
    """
    Gets information about networks on OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about networks
    """
    connection = _get_shade_connection(credentials)
    return []


def get_security_group_info(credentials: Credentials) -> List[Dict]:
    """
    Gets information about security groups on OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about security groups
    """
    connection = _get_shade_connection(credentials)
    return []


def get_volume_info(credentials: Credentials) -> List[Dict]:
    """
    Gets information about volumes (attached and unattached) on OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about volumes
    """
    connection = _get_shade_connection(credentials)
    return []


def get_server_info(credentials: Credentials) -> List[Dict]:
    """
    Gets information about servers on OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about servers
    """
    connection = _get_shade_connection(credentials)
    return connection.list_servers(detailed=True)


def get_openstack_info(credentials: Credentials) -> Dict:
    """
    Gets information about OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about OpenStack
    """
    return {
        OPENSTACK_INSTANCES_JSON_KEY: get_server_info(credentials),
        OPENSTACK_VOLUMES_JSON_KEY: get_volume_info(credentials),
        OPENSTACK_NETWORKS_JSON_KEY: get_security_group_info(credentials),
        OPENSTACK_SECURITY_GROUPS_JSON_KEY: get_network_info(credentials)
    }
