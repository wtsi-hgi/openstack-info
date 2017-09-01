import unittest

from openstackinfo.schema import IndexedByTypeValidator, IndexedByIdValidator, Validator, ValidationError
from openstackinfo.tests._common import INFORMATION_INDEXED_BY_TYPE, INFORMATION_INDEXED_BY_ID


class TestValidator(unittest.TestCase):
    """
    Tests for `Validator`.
    """
    def setUp(self):
        self.valid = None
        self.validator: Validator = type(
            "DummyValidator", (Validator, ), {"get_validity": lambda validator, information: (self.valid, None)})()

    def test_is_valid_when_true(self):
        self.valid = True
        self.assertTrue(self.validator.is_valid({}))

    def test_is_valid_when_false(self):
        self.valid = False
        self.assertFalse(self.validator.is_valid({}))

    def test_ensure_valid_when_valid(self):
        self.valid = True
        self.validator.ensure_valid({})

    def test_ensure_valid_when_invalid(self):
        self.valid = False
        self.assertRaises(ValidationError, self.validator.ensure_valid, {})


class TestIndexedByIdValidator(unittest.TestCase):
    """
    Tests for `IndexedByIdValidator`.
    """
    def setUp(self):
        self.validator = IndexedByIdValidator()

    def test_get_validity_when_valid(self):
        valid, reason = self.validator.get_validity(INFORMATION_INDEXED_BY_ID)
        self.assertTrue(valid)
        self.assertIsNone(reason)

    def test_get_validity_when_invalid(self):
        valid, reason = self.validator.get_validity(INFORMATION_INDEXED_BY_TYPE)
        self.assertFalse(valid)
        self.assertIsNotNone(reason)


class TestIndexedByTypeValidator(unittest.TestCase):
    """
    Tests for `IndexedByTypeValidator`.
    """
    def setUp(self):
        self.validator = IndexedByTypeValidator()

    def test_get_validity_when_valid(self):
        valid, reason = self.validator.get_validity(INFORMATION_INDEXED_BY_TYPE)
        self.assertTrue(valid)
        self.assertIsNone(reason)

    def test_get_validity_when_invalid(self):
        valid, reason = self.validator.get_validity(INFORMATION_INDEXED_BY_ID)
        self.assertFalse(valid)
        self.assertIsNotNone(reason)


if __name__ == "__main__":
    unittest.main()
