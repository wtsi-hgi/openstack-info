import unittest

from openstackinfo.schema import validate, ValidationError, INDEX_BY_TYPE_SCHEMA
from openstackinfo.tests._common import INFORMATION_INDEXED_BY_TYPE


class TestValidate(unittest.TestCase):
    """
    Tests for `validate`.
    """
    def test_valid(self):
        validate("hello", {"type": "string"})

    def test_invalid(self):
        self.assertRaises(ValidationError, validate, 123, {"type": "string"})


class TestSchemas(unittest.TestCase):
    """
    Tests that the schemas are correct, according to the test data.
    """
    def test_index_by_type_schema(self):
        validate(INFORMATION_INDEXED_BY_TYPE, INDEX_BY_TYPE_SCHEMA)


if __name__ == "__main__":
    unittest.main()
