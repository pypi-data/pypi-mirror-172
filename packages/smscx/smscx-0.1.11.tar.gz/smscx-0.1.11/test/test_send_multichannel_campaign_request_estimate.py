import sys
import unittest

import smscx_client
from smscx_client.model.strategy import Strategy
globals()['Strategy'] = Strategy
from smscx_client.model.send_multichannel_campaign_request_estimate import SendMultichannelCampaignRequestEstimate


class TestSendMultichannelCampaignRequestEstimate(unittest.TestCase):
    """SendMultichannelCampaignRequestEstimate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendMultichannelCampaignRequestEstimate(self):
        """Test SendMultichannelCampaignRequestEstimate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendMultichannelCampaignRequestEstimate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
