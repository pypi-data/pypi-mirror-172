import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
globals()['Error'] = Error
from smscx_client.model.model401_invalid_client import Model401InvalidClient


class TestModel401InvalidClient(unittest.TestCase):
    """Model401InvalidClient unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel401InvalidClient(self):
        """Test Model401InvalidClient"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Model401InvalidClient()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
