import json
import os
import sys
from argparse import ArgumentParser

from typing import List, Dict, Callable, NamedTuple

from openstackinfo import Credentials
from openstackinfo.runners import INDEX_BY_TYPE, RunConfiguration, INDEXABLE_BY, get_information

USERNAME_ENVIRONMENT_VARIABLE = "OS_USERNAME"
PASSWORD_ENVIRONMENT_VARIABLE = "OS_PASSWORD"
AUTH_URL_ENVIRONMENT_VARIABLE = "OS_AUTH_URL"
TENANT_ENVIRONMENT_VARIABLE = "OS_TENANT_NAME"


class CliConfiguration(NamedTuple):
    """
    Cli configuration.
    """
    index_by: Callable[[Dict], Dict]


def get_credentials_from_environment() -> Credentials:
    """
    Gets credentials to access OpenStack from the environment.
    :return: credentials.
    :raises KeyError: if a required environment variable has not been set
    """
    return Credentials(
        username=os.environ[USERNAME_ENVIRONMENT_VARIABLE],
        password=os.environ[PASSWORD_ENVIRONMENT_VARIABLE],
        auth_url=os.environ[AUTH_URL_ENVIRONMENT_VARIABLE],
        tenant=os.environ[TENANT_ENVIRONMENT_VARIABLE]
    )


def _parse_arguments(argument_list: List[str]) -> CliConfiguration:
    """
    Parse the given CLI arguments.
    :return: CLI arguments
    """
    parser = ArgumentParser(description="Openstack tenant information retriever")
    parser.add_argument("-i", "--index", default=INDEX_BY_TYPE, choices=list(INDEXABLE_BY.keys()),
                        help="What the OpenStack information should be index by")
    arguments = parser.parse_args(argument_list)
    return CliConfiguration(index_by=INDEXABLE_BY[arguments.index])


def main():
    """
    Entrypoint.
    """
    cli_configuration = _parse_arguments(sys.argv[1:])
    credentials = get_credentials_from_environment()
    information = get_information(RunConfiguration(credentials=credentials, indexer=cli_configuration.index_by))
    print(json.dumps(information, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
