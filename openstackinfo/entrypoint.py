import json
import os
import sys
from argparse import ArgumentParser

from typing import List, Dict, NamedTuple, Type

from openstackinfo.helpers import get_information
from openstackinfo.indexers import InformationIndexerByType, InformationIndexerById
from openstackinfo.models import Credentials, RunConfiguration
from openstackinfo.retrievers import ShadeInformationRetriever, InformationRetriever

USERNAME_ENVIRONMENT_VARIABLE = "OS_USERNAME"
PASSWORD_ENVIRONMENT_VARIABLE = "OS_PASSWORD"
AUTH_URL_ENVIRONMENT_VARIABLE = "OS_AUTH_URL"
TENANT_ENVIRONMENT_VARIABLE = "OS_TENANT_NAME"

SHORT_INDEX_CLI_PARAMETER = "-i"
LONG_INDEX_CLI_PARAMETER = "--index"

INDEX_BY_TYPE = "type"
INDEX_BY_ID = "id"
INDEXER_MAP: Dict[str, Type[InformationRetriever]] = {
    INDEX_BY_TYPE: InformationIndexerByType,
    INDEX_BY_ID: InformationIndexerById
}


class CliConfiguration(NamedTuple):
    """
    CLI configuration.
    """
    indexer: Type[InformationRetriever]


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


def parse_arguments(argument_list: List[str]) -> CliConfiguration:
    """
    Parse the given CLI arguments.
    :return: CLI arguments
    """
    parser = ArgumentParser(description="Openstack tenant information retriever")
    parser.add_argument(SHORT_INDEX_CLI_PARAMETER, LONG_INDEX_CLI_PARAMETER, default=INDEX_BY_TYPE,
                        choices=list(INDEXER_MAP.keys()), help="What the OpenStack information should be index by")
    arguments = parser.parse_args(argument_list)
    return CliConfiguration(indexer=INDEXER_MAP[arguments.index])


def main():
    """
    Entrypoint.
    """
    cli_configuration = parse_arguments(sys.argv[1:])
    credentials = get_credentials_from_environment()
    retriever = ShadeInformationRetriever(credentials)
    information = get_information(RunConfiguration(retriever=retriever, indexer=cli_configuration.indexer))
    print(json.dumps(information, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
