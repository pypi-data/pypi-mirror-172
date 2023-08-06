import sys
import unittest

import smscx_client
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
from smscx_client.model.info_viber import InfoViber


class TestInfoViber(unittest.TestCase):
    """InfoViber unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoViber(self):
        """Test InfoViber"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoViber()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
