import unittest

from openstackinfo.helpers import get_information, RunConfiguration
from openstackinfo.indexers import InformationIndexerById
from openstackinfo.retriever.retrievers import DummyInformationRetriever
from openstackinfo.tests._common import INFORMATION_INDEXED_BY_TYPE, INFORMATION_INDEXED_BY_ID


class TestGetInformation(unittest.TestCase):
    """
    Tests for `get_information`.
    """
    def test_get_information(self):
        configuration = RunConfiguration(
            retriever=DummyInformationRetriever(INFORMATION_INDEXED_BY_TYPE), indexer=InformationIndexerById())
        information = get_information(configuration)
        self.assertEqual(information, INFORMATION_INDEXED_BY_ID)


if __name__ == "__main__":
    unittest.main()
