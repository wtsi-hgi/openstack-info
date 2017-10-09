from typing import NamedTuple


class Credentials(NamedTuple):
    """
    Credentials used to access OpenStack.
    """
    username: str
    password: str
    auth_url: str
    tenant: str


class ConnectionConfiguration(NamedTuple):
    """
    TODO
    """
    max_simultaneous_connections: int = 1
    number_of_retries: int = 0
    retry_period_in_seconds: float = 1.0
    retry_period_multiplier: float = 2.0
