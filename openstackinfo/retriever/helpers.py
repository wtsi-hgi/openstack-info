import logging
from time import sleep

from typing import Callable, List

from openstackinfo.retriever.models import ConnectionConfiguration

logger = logging.getLogger(__name__)


class MaxTriesException(Exception):
    """
    Exception to be raised when a maximum number of tries is exceeded.
    """
    def __init__(self, max_retries: int=0, exceptions: List[Exception]=None):
        """
        Constructor.
        :param max_retries: the maximum number of retires that were allowed
        :param exceptions: the exceptions that were raised after each try (optional)
        """
        self.max_retries = max_retries
        self.exceptions = exceptions
        super().__init__(f"Max request tries reached: {self.max_retries + 1}.%s"
                         % (f" Exceptions: {exceptions}" if exceptions is not None and len(exceptions) > 0 else "", ))


def create_retry_decorator(connection_configuration: ConnectionConfiguration, wait_method: Callable=sleep) -> Callable:
    """
    Creates a retry decorator that is configured using the given connection configuration.
    :param connection_configuration: the configuration for how connection retries are to be conducted
    :param wait_method: method use to wait, where the argument is the wait time in seconds
    :return: the decorator
    """
    def decorator(wrapped: Callable) -> Callable:
        def decorated(*args, **kwargs) -> Callable:
            retry_wait = connection_configuration.retry_wait_in_seconds
            retries = 0
            exceptions: List[Exception] = []

            while retries < connection_configuration.max_retries:
                try:
                    return wrapped(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    logger.error(e)

                    if retries != connection_configuration.max_retries:
                        wait_method(retry_wait)
                        retry_wait *= connection_configuration.retry_wait_multiplier
                        retries += 1

            raise MaxTriesException(retries, exceptions)

        return decorated
    return decorator

