import sys
import unittest

import smscx_client
from smscx_client.model.strategy import Strategy
globals()['Strategy'] = Strategy
from smscx_client.model.send_multichannel_campaign_request import SendMultichannelCampaignRequest


class TestSendMultichannelCampaignRequest(unittest.TestCase):
    """SendMultichannelCampaignRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendMultichannelCampaignRequest(self):
        """Test SendMultichannelCampaignRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendMultichannelCampaignRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
