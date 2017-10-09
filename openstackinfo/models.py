from typing import NamedTuple

from openstackinfo.indexers import InformationIndexerByType, InformationIndexer
from openstackinfo.retriever.retrievers import InformationRetriever


class RunConfiguration(NamedTuple):
    """
    Run configuration.
    """
    retriever: InformationRetriever
    indexer: InformationIndexer = InformationIndexerByType()
