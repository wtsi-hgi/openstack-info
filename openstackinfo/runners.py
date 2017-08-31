from munch import Munch
from typing import NamedTuple, Dict, Callable

from openstackinfo.models import Credentials
from openstackinfo._gathers import get_openstack_info
from openstackinfo.indexers import index_information_by_type, index_information_by_id
from openstackinfo._serialisation import OpenstackJSONEncoder

INDEX_BY_TYPE = "type"
INDEX_BY_ID = "id"
INDEX_BY_FUNCTIONS = {
    INDEX_BY_TYPE: index_information_by_type,
    INDEX_BY_ID: index_information_by_id
}


class RunConfiguration(NamedTuple):
    """
    Run configuration.
    """
    credentials: Credentials
    indexer: Callable[[Dict], Dict] = INDEX_BY_FUNCTIONS[INDEX_BY_TYPE]


def get_information(configuration: RunConfiguration) -> Dict:
    """
    Runs the given confirmation to get information about OpenStack tenant.
    :param configuration: run configuration
    :return: information about OpenStack tenant
    """
    openstack_info = get_openstack_info(configuration.credentials)
    indexed_openstack_info = configuration.indexer(openstack_info)
    return indexed_openstack_info
