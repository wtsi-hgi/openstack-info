import unittest

import os

from openstackinfo.entrypoint import USERNAME_ENVIRONMENT_VARIABLE, PASSWORD_ENVIRONMENT_VARIABLE, \
    AUTH_URL_ENVIRONMENT_VARIABLE, TENANT_ENVIRONMENT_VARIABLE, get_credentials_from_environment, parse_arguments, \
    LONG_INDEX_CLI_PARAMETER
from openstackinfo.helpers import IndexBy
from openstackinfo.indexers import InformationIndexerById
from openstackinfo.tests._common import TEST_USERNAME, TEST_PASSWORD, TEST_AUTH_URL, TEST_TENANT_NAME


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
        configuration = parse_arguments([f"--{LONG_INDEX_CLI_PARAMETER}", IndexBy.ID.value])
        self.assertIsInstance(configuration.indexer, InformationIndexerById)


if __name__ == "__main__":
    unittest.main()
