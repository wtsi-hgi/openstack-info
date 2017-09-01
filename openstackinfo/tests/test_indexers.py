import unittest

from openstackinfo.indexers import InformationIndexerByType, UnsupportedIndexingError, InformationIndexerById
from openstackinfo.schema import IndexedByTypeValidator, IndexedByIdValidator
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
        valid, reason = IndexedByIdValidator().get_validity(information)
        self.assertTrue(valid, msg=reason)


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
        valid, reason = IndexedByTypeValidator().get_validity(information)
        self.assertTrue(valid, msg=reason)


if __name__ == "__main__":
    unittest.main()
