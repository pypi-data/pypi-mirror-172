import sys
import unittest

import smscx_client
from smscx_client.model.custom_fields import CustomFields
globals()['CustomFields'] = CustomFields
from smscx_client.model.send_viber_campaign_request import SendViberCampaignRequest


class TestSendViberCampaignRequest(unittest.TestCase):
    """SendViberCampaignRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendViberCampaignRequest(self):
        """Test SendViberCampaignRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendViberCampaignRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
