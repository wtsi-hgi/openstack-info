import logging

from typing import Callable, List

from openstackinfo.retriever.models import ConnectionConfiguration

_logger = logging.getLogger(__name__)


def retry_wrapper(connection_configuration: ConnectionConfiguration) -> Callable:
    """
    TODO
    :param wrapped:
    :return:
    """
    def decorator(wrapped: Callable) -> Callable:
        def decorated(*args, **kwargs) -> Callable:
            retry_period_in_milliseconds = connection_configuration.retry_period_in_seconds * 1000
            retires = 0
            exceptions: List[Exception] = []

            while retires <= connection_configuration.number_of_retries:
                try:
                    return wrapped(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    _logger.error(e)
                    retry_period_in_milliseconds *= connection_configuration.retry_period_multiplier
                    retires += 1

            raise MaxRetriesException(retires, exceptions)

        return decorated
    return decorator


class MaxRetriesException(Exception):
    """
    TODO
    """
    def __init__(self, retries: int=0, exceptions: List[Exception]=None):
        """
        TODO
        :param retries:
        :param exceptions:
        """
        self.retries = retries
        self.exceptions = exceptions if exceptions is not None else []
        super().__init__(f"Max request retries reached: {self.retries}. Exceptions: {exceptions}")
