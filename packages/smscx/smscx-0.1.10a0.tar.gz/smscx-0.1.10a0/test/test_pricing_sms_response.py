import sys
import unittest

import smscx_client
from smscx_client.model.network_operator import NetworkOperator
globals()['NetworkOperator'] = NetworkOperator
from smscx_client.model.pricing_sms_response import PricingSmsResponse


class TestPricingSmsResponse(unittest.TestCase):
    """PricingSmsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPricingSmsResponse(self):
        """Test PricingSmsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = PricingSmsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
