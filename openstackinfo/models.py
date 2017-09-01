from typing import NamedTuple, List, Dict, Type

from openstackinfo.indexers import InformationIndexer, InformationIndexerByType
from openstackinfo.retrievers import InformationRetriever


class Credentials(NamedTuple):
    """
    Credentials used to access OpenStack.
    """
    username: str
    password: str
    auth_url: str
    tenant: str


class RunConfiguration(NamedTuple):
    """
    Run configuration.
    """
    retriever: InformationRetriever
    indexer: Type[InformationIndexer] = InformationIndexerByType