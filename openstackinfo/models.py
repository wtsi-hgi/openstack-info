from openstack.block_store.v2.volume import VolumeDetail
from openstack.compute.v2.server import Server
from openstack.network.v2.network import Network
from openstack.network.v2.security_group import SecurityGroup
from typing import NamedTuple, List


class Credentials(NamedTuple):
    """
    Credentials used to access OpenStack.
    """
    username: str
    password: str
    auth_url: str
    tenant: str


class Openstack():
    """
    Openstack information.
    """
    def __init__(self, volumes: List[VolumeDetail]=None, servers: List[Server]=None,
                 security_groups: List[SecurityGroup]=None, networks: List[Network]=None):
        self.volumes = volumes if volumes is not None else []
        self.servers = servers if servers is not None else []
        self.security_groups = security_groups if security_groups is not None else []
        self.networks = networks if networks is not None else []
