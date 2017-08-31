import json
import os
from argparse import ArgumentParser

import sys
from typing import List, NamedTuple, Dict, Callable

from openstackinfo import index_information_by_id
from openstackinfo.gathers import get_openstack_info

from openstackinfo.indexers import index_information_by_type
from openstackinfo.models import Credentials
from openstackinfo.serialisation import OpenstackJSONEncoder

USERNAME_ENVIRONMENT_VARIABLE = "OS_USERNAME"
PASSWORD_ENVIRONMENT_VARIABLE = "OS_PASSWORD"
AUTH_URL_ENVIRONMENT_VARIABLE = "OS_AUTH_URL"
TENANT_ENVIRONMENT_VARIABLE = "OS_TENANT_NAME"

_INDEX_BY_TYPE_OPTION = "type"
_INDEX_BY_ID_OPTION = "id"
_INDEX_BY_FUNCTIONS = {
    _INDEX_BY_TYPE_OPTION: index_information_by_type,
    _INDEX_BY_ID_OPTION: index_information_by_id
}


class _Configuration(NamedTuple):
    """
    Run configuration.
    """
    index_by: Callable[[Dict], Dict] = _INDEX_BY_FUNCTIONS[_INDEX_BY_TYPE_OPTION]


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


def _parse_arguments(argument_list: List[str]) -> _Configuration:
    """
    Parse the given CLI arguments.
    :return: CLI arguments
    """
    parser = ArgumentParser(description="Openstack tenant information retriever")
    parser.add_argument("-i", "--index", default=_INDEX_BY_TYPE_OPTION, choices=list(_INDEX_BY_FUNCTIONS.keys()),
                        help="What the OpenStack information should be index by")
    arguments = parser.parse_args(argument_list)
    return _Configuration(index_by=_INDEX_BY_FUNCTIONS[arguments.index])


def main():
    """
    Entrypoint.
    """
    configuration = _parse_arguments(sys.argv[1:])
    credentials = get_credentials_from_environment()
    openstack_info = get_openstack_info(credentials)
    openstack_info_as_json = OpenstackJSONEncoder().default(openstack_info)
    indexed_openstack_info_as_json = configuration.index_by(openstack_info_as_json)
    print(json.dumps(indexed_openstack_info_as_json, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
