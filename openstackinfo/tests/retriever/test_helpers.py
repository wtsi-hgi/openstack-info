import logging
import unittest
from typing import List

from openstackinfo.retriever.helpers import create_retry_decorator, MaxRetriesException, logger
from openstackinfo.retriever.models import ConnectionConfiguration


class _CustomException(Exception):
    """
    Custom exception.
    """


class TestCreateRetryDecorator(unittest.TestCase):
    """
    Tests for `create_retry_decorator`.
    """
    @classmethod
    def setUpClass(cls):
        logger.setLevel(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logger.setLevel(logging.NOTSET)

    def test_retry_times(self):
        connection_configuration = ConnectionConfiguration(max_retries=3, retry_wait_in_seconds=0)
        runs = 0

        @create_retry_decorator(connection_configuration)
        def example():
            nonlocal runs
            runs += 1
            raise _CustomException()

        exception = None
        try:
            example()
        except MaxRetriesException as e:
            exception = e

        self.assertIsNotNone(exception)
        self.assertEqual(connection_configuration.max_retries, exception.retries)
        self.assertEqual(3, len(exception.exceptions))
        self.assertIsInstance(exception.exceptions[0], _CustomException)

    def test_retry_waits(self):
        connection_configuration = ConnectionConfiguration(
            max_retries=6, retry_wait_in_seconds=2.0, retry_wait_multiplier=5)
        wait_times: List[int] = []

        def wait_method(wait_time: int):
            wait_times.append(wait_time)

        @create_retry_decorator(connection_configuration, wait_method)
        def example():
            raise _CustomException()

        self.assertRaises(MaxRetriesException, example)
        self.assertEqual(
            [(connection_configuration.retry_wait_in_seconds * connection_configuration.retry_wait_multiplier ** i)
             * 1000 for i in range(connection_configuration.max_retries)], wait_times)


if __name__ == "__main__":
    unittest.main()
