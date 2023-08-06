import sys
import unittest

import smscx_client
from smscx_client.model.data_multichannel import DataMultichannel
from smscx_client.model.info_multichannel_campaign import InfoMultichannelCampaign
globals()['DataMultichannel'] = DataMultichannel
globals()['InfoMultichannelCampaign'] = InfoMultichannelCampaign
from smscx_client.model.send_multichannel_campaign_response import SendMultichannelCampaignResponse


class TestSendMultichannelCampaignResponse(unittest.TestCase):
    """SendMultichannelCampaignResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendMultichannelCampaignResponse(self):
        """Test SendMultichannelCampaignResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendMultichannelCampaignResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
