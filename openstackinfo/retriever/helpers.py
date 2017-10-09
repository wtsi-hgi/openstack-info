import logging
from time import sleep

from typing import Callable, List

from openstackinfo.retriever.models import ConnectionConfiguration

logger = logging.getLogger(__name__)


class MaxRetriesException(Exception):
    """
    Exception to be raised when a maximum number of retries is exceeded.
    """
    def __init__(self, retries: int=0, exceptions: List[Exception]=None):
        """
        Constructor.
        :param retries: the number of retires that have been conducted
        :param exceptions: the exceptions that were raised after each retry (optional)
        """
        self.retries = retries
        self.exceptions = exceptions
        super().__init__(f"Max request retries reached: {self.retries}.%s"
                         % (f"Exceptions: {exceptions}" if exceptions is not None else "", ))


def create_retry_decorator(connection_configuration: ConnectionConfiguration, wait_method: Callable=sleep) -> Callable:
    """
    Creates a retry decorator that is configured using the given connection configuration.
    :param connection_configuration: the configuration for how connection retries are to be conducted
    :param wait_method: method use to wait
    :return: the decorator
    """
    def decorator(wrapped: Callable) -> Callable:
        def decorated(*args, **kwargs) -> Callable:
            retry_wait_in_milliseconds = connection_configuration.retry_wait_in_seconds * 1000
            retires = 0
            exceptions: List[Exception] = []

            while retires < connection_configuration.max_retries:
                try:
                    return wrapped(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    logger.error(e)
                    wait_method(retry_wait_in_milliseconds)
                    retry_wait_in_milliseconds *= connection_configuration.retry_wait_multiplier
                    retires += 1

            raise MaxRetriesException(retires, exceptions)

        return decorated
    return decorator

