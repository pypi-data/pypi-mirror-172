import sys
import unittest

import smscx_client
from smscx_client.model.data_available_numbers_rent import DataAvailableNumbersRent
globals()['DataAvailableNumbersRent'] = DataAvailableNumbersRent
from smscx_client.model.rent_numbers_response import RentNumbersResponse


class TestRentNumbersResponse(unittest.TestCase):
    """RentNumbersResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRentNumbersResponse(self):
        """Test RentNumbersResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = RentNumbersResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
