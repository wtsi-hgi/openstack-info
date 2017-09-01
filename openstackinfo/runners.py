from typing import NamedTuple, Dict, Type

from openstackinfo._gathers import ShadeInformationGatherer
from openstackinfo.indexers import InformationIndexerById, InformationIndexerByType, InformationIndexer
from openstackinfo.models import Credentials

INDEX_BY_TYPE = "type"
INDEX_BY_ID = "id"
INDEXER_MAP = {
    INDEX_BY_TYPE: InformationIndexerByType,
    INDEX_BY_ID: InformationIndexerById
}


class RunConfiguration(NamedTuple):
    """
    Run configuration.
    """
    credentials: Credentials
    indexer: Type[InformationIndexer] = INDEXER_MAP[INDEX_BY_TYPE]


def get_information(configuration: RunConfiguration) -> Dict:
    """
    Runs the given confirmation to get information about OpenStack tenant.
    :param configuration: run configuration
    :return: information about OpenStack tenant
    """
    gatherer = ShadeInformationGatherer(configuration.credentials)
    openstack_info = gatherer.get_openstack_info()
    indexed_openstack_info = configuration.indexer().index(openstack_info)
    return indexed_openstack_info
