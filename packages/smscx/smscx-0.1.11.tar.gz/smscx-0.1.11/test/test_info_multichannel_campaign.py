import sys
import unittest

import smscx_client
from smscx_client.model.group import Group
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
globals()['Group'] = Group
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
from smscx_client.model.info_multichannel_campaign import InfoMultichannelCampaign


class TestInfoMultichannelCampaign(unittest.TestCase):
    """InfoMultichannelCampaign unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoMultichannelCampaign(self):
        """Test InfoMultichannelCampaign"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoMultichannelCampaign()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
