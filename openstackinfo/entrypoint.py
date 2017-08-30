import json
import os
from typing import List, Dict

from novaclient.client import Client as NovaClient
from novaclient.v2.servers import Server

from openstackinfo.models import Credentials
from openstackinfo.serialisation import ServerJSONEncoder

DEFAULT_NOVA_VERSION = "2"

USERNAME_ENVIRONMENT_VARIABLE = "OS_USERNAME"
PASSWORD_ENVIRONMENT_VARIABLE = "OS_PASSWORD"
AUTH_URL_ENVIRONMENT_VARIABLE = "OS_AUTH_URL"
TENANT_ENVIRONMENT_VARIABLE = "OS_TENANT_NAME"


def get_server_list(credentials: Credentials, nova_version: str=DEFAULT_NOVA_VERSION) -> List[Server]:
    """
    TODO
    :param credentials:
    :param nova_version:
    :return:
    """
    client = NovaClient(nova_version, credentials.username, credentials.password, project_name=credentials.tenant,
                        auth_url=credentials.auth_url)
    servers = client.servers.list()

    for server in servers:
        security_groups = client.servers.list_security_group(server.id)
        server.security_groups = security_groups

    return servers


def get_data() -> Dict:
    """
    TODO
    :return:
    """
    credentials = get_credentials_from_environment()
    servers = get_server_list(credentials)
    return ServerJSONEncoder().default(servers)


def get_credentials_from_environment() -> Credentials:
    """
    TODO
    :return:
    """
    return Credentials(
        username=os.environ[USERNAME_ENVIRONMENT_VARIABLE],
        password=os.environ[PASSWORD_ENVIRONMENT_VARIABLE],
        auth_url=os.environ[AUTH_URL_ENVIRONMENT_VARIABLE],
        tenant=os.environ[TENANT_ENVIRONMENT_VARIABLE],
    )


def main():
    """
    TODO
    :return:
    """
    credentials = get_credentials_from_environment()
    servers = get_server_list(credentials)
    print(json.dumps(servers, cls=ServerJSONEncoder, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
