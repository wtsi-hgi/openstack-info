from novaclient.client import Client as NovaClient
from novaclient.v2.servers import Server
from openstack import profile
from openstack.connection import Connection
from typing import List

from openstackinfo.models import Openstack, Credentials

NOVA_VERSION = "2"

_connection_cache = None


def _get_connection(credentials: Credentials) -> Connection:
    """
    Gets OpenStack SDK connection to OpenStack using the given credentials.

    The connection is cached and shared.
    :param credentials: credentials used to access OpenStack API
    :return: OpenStack SDK connection (may or may not be authorised)
    """
    global _connection_cache
    if _connection_cache is None:
        _connection_cache = Connection(
            profile=profile.Profile(),
            auth_url=credentials.auth_url,
            project_name=credentials.tenant,
            username=credentials.username,
            password=credentials.password
        )
    return _connection_cache


def get_network_info(credentials: Credentials):
    """
    Gets information about networks on OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about networks
    """
    connection = _get_connection(credentials)
    return list(connection.network.networks())


def get_security_group_info(credentials: Credentials):
    """
    Gets information about security groups on OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about security groups
    """
    connection = _get_connection(credentials)
    return list(connection.network.security_groups())


def get_volume_info(credentials: Credentials):
    """
    Gets information about volumes (attached and unattached) on OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about volumes
    """
    connection = _get_connection(credentials)
    return list(connection.block_store.volumes())


def get_server_info(credentials: Credentials) -> List[Server]:
    """
    Gets information about servers on OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about servers
    """
    connection = _get_connection(credentials)
    servers = list(connection.compute.servers())

    # Note: openstacksdk==0.9.18 does not offer a way to get the IDs of a security group associated to an instance: it
    # incorrectly assumes that the name is unique.
    nova_client = NovaClient(NOVA_VERSION, username=credentials.username, password=credentials.password,
                             project_name=credentials.tenant, auth_url=credentials.auth_url)
    for server in servers:
        security_groups = nova_client.servers.list_security_group(server.id)
        server.security_groups = security_groups

        if server.networks is None:
            server.networks = []

    return servers


def get_openstack_info(credentials: Credentials) -> Openstack:
    """
    Gets information about OpenStack.
    :param credentials: credentials used to access OpenStack API
    :return: information about OpenStack
    """
    return Openstack(
        servers=get_server_info(credentials),
        volumes=get_volume_info(credentials),
        security_groups=get_security_group_info(credentials),
        networks=get_network_info(credentials)
    )
