import sys
import unittest

import smscx_client
from smscx_client.model.info_rent_number import InfoRentNumber
globals()['InfoRentNumber'] = InfoRentNumber
from smscx_client.model.rent_number_response import RentNumberResponse


class TestRentNumberResponse(unittest.TestCase):
    """RentNumberResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRentNumberResponse(self):
        """Test RentNumberResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = RentNumberResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
