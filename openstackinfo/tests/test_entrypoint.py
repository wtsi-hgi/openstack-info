import unittest

import os

from openstackinfo.entrypoint import USERNAME_ENVIRONMENT_VARIABLE, PASSWORD_ENVIRONMENT_VARIABLE, \
    AUTH_URL_ENVIRONMENT_VARIABLE, TENANT_ENVIRONMENT_VARIABLE, get_credentials_from_environment, parse_arguments, \
    LONG_INDEX_CLI_PARAMETER, LONG_MAX_CONNECTIONS_CLI_PARAMETER, LONG_MAX_RETRIES_CLI_PARAMETER, \
    LONG_RETRY_WAIT_IN_SECONDS_CLI_PARAMETER, LONG_RETRY_WAIT_MULTIPLIER_CLI_PARAMETER
from openstackinfo.helpers import IndexBy
from openstackinfo.indexers import InformationIndexerById
from openstackinfo.tests._common import TEST_USERNAME, TEST_PASSWORD, TEST_AUTH_URL, TEST_TENANT_NAME, \
    TEST_MAX_CONNECTIONS, TEST_MAX_RETIRES, TEST_RETRY_WAIT_IN_SECONDS, TEST_RETRY_WAIT_MULTIPLIER


class TestGetCredentialsFromEnvironment(unittest.TestCase):
    """
    Tests for `get_credentials_from_environment`.
    """
    def test_when_invalid_environment(self):
        self.assertRaises(KeyError, get_credentials_from_environment)

    def test_when_valid_environment(self):
        os.environ[USERNAME_ENVIRONMENT_VARIABLE] = TEST_USERNAME
        os.environ[PASSWORD_ENVIRONMENT_VARIABLE] = TEST_PASSWORD
        os.environ[AUTH_URL_ENVIRONMENT_VARIABLE] = TEST_AUTH_URL
        os.environ[TENANT_ENVIRONMENT_VARIABLE] = TEST_TENANT_NAME
        credentials = get_credentials_from_environment()
        self.assertEqual(TEST_USERNAME, credentials.username)
        self.assertEqual(TEST_PASSWORD, credentials.password)
        self.assertEqual(TEST_AUTH_URL, credentials.auth_url)
        self.assertEqual(TEST_TENANT_NAME, credentials.tenant)


class TestParseArguments(unittest.TestCase):
    """
    Tests for `parse_arguments`.
    """
    def test_when_valid_arguments(self):
        configuration = parse_arguments([str(x) for x in [
            f"--{LONG_INDEX_CLI_PARAMETER}", IndexBy.ID.value,
            f"--{LONG_MAX_CONNECTIONS_CLI_PARAMETER}", TEST_MAX_CONNECTIONS,
            f"--{LONG_MAX_RETRIES_CLI_PARAMETER}", TEST_MAX_RETIRES,
            f"--{LONG_RETRY_WAIT_IN_SECONDS_CLI_PARAMETER}", TEST_RETRY_WAIT_IN_SECONDS,
            f"--{LONG_RETRY_WAIT_MULTIPLIER_CLI_PARAMETER}", TEST_RETRY_WAIT_MULTIPLIER
        ]])
        self.assertIsInstance(configuration.indexer, InformationIndexerById)
        self.assertEqual(TEST_MAX_CONNECTIONS, configuration.connection_configuration.max_connections)
        self.assertEqual(TEST_MAX_RETIRES, configuration.connection_configuration.max_retries)
        self.assertEqual(TEST_RETRY_WAIT_IN_SECONDS, configuration.connection_configuration.retry_wait_in_seconds)
        self.assertEqual(TEST_RETRY_WAIT_MULTIPLIER, configuration.connection_configuration.retry_wait_multiplier)


if __name__ == "__main__":
    unittest.main()
