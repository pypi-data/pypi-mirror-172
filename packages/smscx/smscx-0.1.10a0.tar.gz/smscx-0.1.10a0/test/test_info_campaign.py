import sys
import unittest

import smscx_client
from smscx_client.model.group import Group
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
from smscx_client.model.transliteration_analysis import TransliterationAnalysis
globals()['Group'] = Group
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
globals()['TransliterationAnalysis'] = TransliterationAnalysis
from smscx_client.model.info_campaign import InfoCampaign


class TestInfoCampaign(unittest.TestCase):
    """InfoCampaign unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoCampaign(self):
        """Test InfoCampaign"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoCampaign()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
