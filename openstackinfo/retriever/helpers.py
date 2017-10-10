import logging
import random
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


def create_retry_decorator(connection_configuration: ConnectionConfiguration, wait_method: Callable=sleep,
                           randomness_generator: Callable[[float, float], float]=random.uniform) -> Callable:
    """
    Creates a retry decorator that is configured using the given connection configuration.
    :param connection_configuration: the configuration for how connection retries are to be conducted
    :param wait_method: method use to wait, where the argument is the wait time in seconds
    :param randomness_generator: generator of randomness between the two given floats
    :return: the decorator
    """
    def decorator(wrapped: Callable) -> Callable:
        def decorated(*args, **kwargs) -> Callable:
            retry_wait_max_deviation_fraction = connection_configuration.retry_wait_max_deviation_percentage / 100
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
                        if retry_wait_max_deviation_fraction != 0:
                            retry_wait = randomness_generator(
                                retry_wait - retry_wait * retry_wait_max_deviation_fraction,
                                retry_wait + retry_wait * retry_wait_max_deviation_fraction)

                        # TODO: log as info but configure ability to add verbosity on CLI
                        logger.error(f"Waiting for {retry_wait} seconds before next run")
                        wait_method(retry_wait)
                        retry_wait *= connection_configuration.retry_wait_multiplier
                        retries += 1

            raise MaxTriesException(retries, exceptions)

        return decorated
    return decorator

