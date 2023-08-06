import sys
import unittest

import smscx_client
from smscx_client.model.data_number_lookup import DataNumberLookup
globals()['DataNumberLookup'] = DataNumberLookup
from smscx_client.model.number_lookup_response import NumberLookupResponse


class TestNumberLookupResponse(unittest.TestCase):
    """NumberLookupResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNumberLookupResponse(self):
        """Test NumberLookupResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = NumberLookupResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
