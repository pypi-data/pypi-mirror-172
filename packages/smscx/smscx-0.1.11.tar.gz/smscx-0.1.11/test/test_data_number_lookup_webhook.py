import sys
import unittest

import smscx_client
from smscx_client.model.original_network import OriginalNetwork
from smscx_client.model.ported_network import PortedNetwork
from smscx_client.model.roaming_network import RoamingNetwork
globals()['OriginalNetwork'] = OriginalNetwork
globals()['PortedNetwork'] = PortedNetwork
globals()['RoamingNetwork'] = RoamingNetwork
from smscx_client.model.data_number_lookup_webhook import DataNumberLookupWebhook


class TestDataNumberLookupWebhook(unittest.TestCase):
    """DataNumberLookupWebhook unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataNumberLookupWebhook(self):
        """Test DataNumberLookupWebhook"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataNumberLookupWebhook()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
