from typing import NamedTuple, Optional


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
    Configuration for how to manage connection to OpenStack.
    """
    max_connections: Optional[int] = None
    max_retries: int = 2
    retry_wait_in_seconds: float = 1.0
    retry_wait_multiplier: float = 5.0
