from typing import NamedTuple, List, Dict


class Openstack:
    """
    Openstack information.
    """
    def __init__(self, volumes: List[Dict]=None, servers: List[Dict]=None,
                 security_groups: List[Dict]=None, networks: List[Dict]=None):
        self.volumes = volumes if volumes is not None else []
        self.servers = servers if servers is not None else []
        self.security_groups = security_groups if security_groups is not None else []
        self.networks = networks if networks is not None else []


class Credentials(NamedTuple):
    """
    Credentials used to access OpenStack.
    """
    username: str
    password: str
    auth_url: str
    tenant: str
