import json
import os
import sys
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter

from typing import List, NamedTuple, Type, Any

from openstackinfo.helpers import get_information, INDEXER_MAP, IndexBy, RunConfiguration
from openstackinfo.indexers import InformationIndexer
from openstackinfo.retriever.models import ConnectionConfiguration, Credentials
from openstackinfo.retriever.retrievers import ShadeInformationRetriever

USERNAME_ENVIRONMENT_VARIABLE = "OS_USERNAME"
PASSWORD_ENVIRONMENT_VARIABLE = "OS_PASSWORD"
AUTH_URL_ENVIRONMENT_VARIABLE = "OS_AUTH_URL"
TENANT_ENVIRONMENT_VARIABLE = "OS_TENANT_NAME"

SHORT_INDEX_CLI_PARAMETER = "i"
LONG_INDEX_CLI_PARAMETER = "index"

LONG_MAX_CONNECTIONS_CLI_PARAMETER = "max-connections"
LONG_MAX_RETRIES_CLI_PARAMETER = "retries"
LONG_RETRY_WAIT_IN_SECONDS_CLI_PARAMETER = "retry-wait"
LONG_RETRY_WAIT_MULTIPLIER_CLI_PARAMETER = "retry-wait-multiplier"


class CliConfiguration(NamedTuple):
    """
    CLI configuration.
    """
    indexer: Type[InformationIndexer]
    connection_configuration: ConnectionConfiguration


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
    :return: CLI configuration
    """
    parser = ArgumentParser(
        description="Openstack tenant information retriever", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(f"-{SHORT_INDEX_CLI_PARAMETER}", f"--{LONG_INDEX_CLI_PARAMETER}", default=IndexBy.TYPE.value,
                        choices=[item.value for item in IndexBy],
                        help=f"What the OpenStack information should be index by")
    parser.add_argument(f"--{LONG_MAX_CONNECTIONS_CLI_PARAMETER}",
                        default=ConnectionConfiguration().max_connections, type=int,
                        help=f"Maximum number of simultaneous connections to make to OpenStack")
    parser.add_argument(f"--{LONG_MAX_RETRIES_CLI_PARAMETER}",
                        default=ConnectionConfiguration().max_retries, type=float,
                        help="Number of times to retry getting information about a particular tpye of OpenStack "
                             "resource")
    parser.add_argument(f"--{LONG_RETRY_WAIT_IN_SECONDS_CLI_PARAMETER}",
                        default=ConnectionConfiguration().retry_wait_in_seconds, type=float,
                        help="Initial amount of time (in seconds) to wait after a failure before a retry")
    parser.add_argument(f"--{LONG_RETRY_WAIT_MULTIPLIER_CLI_PARAMETER}",
                        default=ConnectionConfiguration().retry_wait_multiplier, type=float,
                        help="Multiplier that is applied to the wait time after each failure")

    cli_input = parser.parse_args(argument_list)
    index_by = IndexBy(_get_parameter_argument(LONG_INDEX_CLI_PARAMETER, cli_input))
    indexer = INDEXER_MAP[index_by]()
    connection_configuration = ConnectionConfiguration(
        max_connections=_get_parameter_argument(LONG_MAX_CONNECTIONS_CLI_PARAMETER, cli_input),
        max_retries=_get_parameter_argument(LONG_MAX_RETRIES_CLI_PARAMETER, cli_input),
        retry_wait_in_seconds=_get_parameter_argument(LONG_RETRY_WAIT_IN_SECONDS_CLI_PARAMETER, cli_input),
        retry_wait_multiplier=_get_parameter_argument(LONG_RETRY_WAIT_MULTIPLIER_CLI_PARAMETER, cli_input)
    )
    return CliConfiguration(indexer=indexer, connection_configuration=connection_configuration)


def _get_parameter_argument(parameter: str, cli_input: Namespace) -> Any:
    """
    Gets the argument associated to the given parameter in the given parsed CLI input.
    :param parameter: the parameter of interest
    :param cli_input: the namespace resulting in the parsing of the CLI input
    :return: the associated argument
    """
    return vars(cli_input)[parameter.replace("-", "_")]


def main():
    """
    Entrypoint.
    """
    cli_configuration = parse_arguments(sys.argv[1:])
    credentials = get_credentials_from_environment()
    retriever = ShadeInformationRetriever(
        credentials, connection_configuration=cli_configuration.connection_configuration)
    information = get_information(RunConfiguration(retriever=retriever, indexer=cli_configuration.indexer))
    print(json.dumps(information, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
