import json
import os

from openstackinfo.gather import get_openstack_info
from openstackinfo.models import Credentials
from openstackinfo.serialisation import OpenstackJSONEncoder

USERNAME_ENVIRONMENT_VARIABLE = "OS_USERNAME"
PASSWORD_ENVIRONMENT_VARIABLE = "OS_PASSWORD"
AUTH_URL_ENVIRONMENT_VARIABLE = "OS_AUTH_URL"
TENANT_ENVIRONMENT_VARIABLE = "OS_TENANT_NAME"


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


def main():
    """
    Entrypoint.
    """
    credentials = get_credentials_from_environment()
    openstack_info = get_openstack_info(credentials)
    print(json.dumps(openstack_info, cls=OpenstackJSONEncoder, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
