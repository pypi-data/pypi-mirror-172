import sys
import unittest

import smscx_client
from smscx_client.model.attachments import Attachments
from smscx_client.model.lookup import Lookup
from smscx_client.model.multichannel import Multichannel
from smscx_client.model.optouts import Optouts
from smscx_client.model.otp import Otp
from smscx_client.model.shortlinks import Shortlinks
from smscx_client.model.sms import Sms
from smscx_client.model.viber import Viber
from smscx_client.model.whatsapp import Whatsapp
globals()['Attachments'] = Attachments
globals()['Lookup'] = Lookup
globals()['Multichannel'] = Multichannel
globals()['Optouts'] = Optouts
globals()['Otp'] = Otp
globals()['Shortlinks'] = Shortlinks
globals()['Sms'] = Sms
globals()['Viber'] = Viber
globals()['Whatsapp'] = Whatsapp
from smscx_client.model.settings import Settings


class TestSettings(unittest.TestCase):
    """Settings unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSettings(self):
        """Test Settings"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Settings()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
