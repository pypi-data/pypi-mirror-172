import sys
import unittest

import smscx_client
from smscx_client.model.transliteration import Transliteration
globals()['Transliteration'] = Transliteration
from smscx_client.model.send_sms_campaign_request import SendSmsCampaignRequest


class TestSendSmsCampaignRequest(unittest.TestCase):
    """SendSmsCampaignRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendSmsCampaignRequest(self):
        """Test SendSmsCampaignRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendSmsCampaignRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
