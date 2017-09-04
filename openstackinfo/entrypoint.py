import json
import os
import sys
from argparse import ArgumentParser

from typing import List, NamedTuple, Type

from openstackinfo.helpers import get_information, INDEXER_MAP, IndexBy
from openstackinfo.indexers import InformationIndexer
from openstackinfo.models import Credentials, RunConfiguration
from openstackinfo.retrievers import ShadeInformationRetriever

USERNAME_ENVIRONMENT_VARIABLE = "OS_USERNAME"
PASSWORD_ENVIRONMENT_VARIABLE = "OS_PASSWORD"
AUTH_URL_ENVIRONMENT_VARIABLE = "OS_AUTH_URL"
TENANT_ENVIRONMENT_VARIABLE = "OS_TENANT_NAME"

SHORT_INDEX_CLI_PARAMETER = "-i"
LONG_INDEX_CLI_PARAMETER = "--index"


class CliConfiguration(NamedTuple):
    """
    CLI configuration.
    """
    indexer: Type[InformationIndexer]


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
    parser.add_argument(
        SHORT_INDEX_CLI_PARAMETER, LONG_INDEX_CLI_PARAMETER, default=IndexBy.TYPE.value,
        choices=[item.value for item in IndexBy], help="What the OpenStack information should be index by")
    arguments = parser.parse_args(argument_list)
    index_by = IndexBy(arguments.index)
    return CliConfiguration(indexer=INDEXER_MAP[index_by]())


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
