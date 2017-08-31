from typing import NamedTuple, Dict, Callable

from openstackinfo import Credentials
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
    index_by: Callable[[Dict], Dict]=INDEX_BY_FUNCTIONS[INDEX_BY_TYPE]


def get_information(configuration: RunConfiguration) -> Dict:
    """
    Runs the given confirmation to get information about OpenStack tenant.
    :param configuration: run configuration
    :return:
    """
    openstack_info = get_openstack_info(configuration.credentials)
    openstack_info_as_json = OpenstackJSONEncoder().default(openstack_info)
    indexed_openstack_info_as_json = configuration.index_by(openstack_info_as_json)
    return indexed_openstack_info_as_json
