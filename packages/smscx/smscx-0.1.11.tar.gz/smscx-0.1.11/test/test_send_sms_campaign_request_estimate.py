import sys
import unittest

import smscx_client
from smscx_client.model.transliteration import Transliteration
globals()['Transliteration'] = Transliteration
from smscx_client.model.send_sms_campaign_request_estimate import SendSmsCampaignRequestEstimate


class TestSendSmsCampaignRequestEstimate(unittest.TestCase):
    """SendSmsCampaignRequestEstimate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendSmsCampaignRequestEstimate(self):
        """Test SendSmsCampaignRequestEstimate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendSmsCampaignRequestEstimate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
