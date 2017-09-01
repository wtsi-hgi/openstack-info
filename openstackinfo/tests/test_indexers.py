import unittest

from openstackinfo.indexers import InformationIndexerByType, UnsupportedIndexingError, InformationIndexerById
from openstackinfo.schema import validate, INDEX_BY_TYPE_SCHEMA
from openstackinfo.tests._common import INFORMATION_INDEXED_BY_TYPE, INFORMATION_INDEXED_BY_ID


class TestInformationIndexerById(unittest.TestCase):
    """
    Tests for `InformationIndexerById`.
    """
    def setUp(self):
        self.indexer = InformationIndexerById()

    def test_when_indexed_by_id(self):
        self.assertRaises(UnsupportedIndexingError, self.indexer.index, INFORMATION_INDEXED_BY_ID)

    def test_when_indexed_by_type(self):
        information = self.indexer.index(INFORMATION_INDEXED_BY_TYPE)
        # TODO: Assert correct!


class TestInformationIndexerByType(unittest.TestCase):
    """
    Tests for `InformationIndexerByType`.
    """
    def setUp(self):
        self.indexer = InformationIndexerByType()

    def test_when_indexed_by_id(self):
        self.assertRaises(UnsupportedIndexingError, self.indexer.index, INFORMATION_INDEXED_BY_ID)

    def test_when_indexed_by_type(self):
        information = self.indexer.index(INFORMATION_INDEXED_BY_TYPE)
        validate(information, INDEX_BY_TYPE_SCHEMA)


if __name__ == "__main__":
    unittest.main()
