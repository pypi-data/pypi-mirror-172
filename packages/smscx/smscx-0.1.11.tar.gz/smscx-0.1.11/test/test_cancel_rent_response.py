import sys
import unittest

import smscx_client
from smscx_client.model.info_cancel_rent import InfoCancelRent
globals()['InfoCancelRent'] = InfoCancelRent
from smscx_client.model.cancel_rent_response import CancelRentResponse


class TestCancelRentResponse(unittest.TestCase):
    """CancelRentResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCancelRentResponse(self):
        """Test CancelRentResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CancelRentResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
