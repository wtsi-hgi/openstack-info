from enum import Enum, unique

from typing import Dict, Type

from openstackinfo.indexers import InformationIndexer, InformationIndexerByType, InformationIndexerById
from openstackinfo.models import RunConfiguration


@unique
class IndexBy(Enum):
    """
    Property by which information can be indexed.
    """
    TYPE = "type"
    ID = "id"


INDEXER_MAP: Dict[str, Type[InformationIndexer]] = {
    IndexBy.TYPE: InformationIndexerByType,
    IndexBy.ID: InformationIndexerById
}


def get_information(configuration: RunConfiguration) -> Dict:
    """
    Runs the given confirmation to get information about OpenStack tenant.
    :param configuration: run configuration
    :return: information about OpenStack tenant
    """
    openstack_info = configuration.retriever.get_openstack_info()
    indexed_openstack_info = configuration.indexer.index(openstack_info)
    return indexed_openstack_info
