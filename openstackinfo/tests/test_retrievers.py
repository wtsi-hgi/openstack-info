import unittest

from openstackinfo.models import Credentials
from openstackinfo.retrievers import ShadeInformationRetriever, DummyInformationRetriever


class TestShadeInformationRetriever(unittest.TestCase):
    """
    Tests for `ShadeInformationRetriever`.
    """
    def test_instantiate(self):
        ShadeInformationRetriever(Credentials("", "", "", ""))

    # XXX: Not much else can be tested until we have a good way to start an OpenStack test environment.


class TestDummyInformationRetriever(unittest.TestCase):
    """
    Tests for `DummyInformationRetriever`.
    """
    def test_instantiate(self):
        DummyInformationRetriever()


if __name__ == "__main__":
    unittest.main()
