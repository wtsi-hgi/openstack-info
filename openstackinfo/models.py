from typing import NamedTuple, Type


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
    from openstackinfo.indexers import InformationIndexer, InformationIndexerByType
    from openstackinfo.retrievers import InformationRetriever

    retriever: InformationRetriever
    indexer: Type[InformationIndexer] = InformationIndexerByType
