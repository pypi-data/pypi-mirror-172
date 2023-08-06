import sys
import unittest

import smscx_client
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
from smscx_client.model.info_conversation_reply import InfoConversationReply


class TestInfoConversationReply(unittest.TestCase):
    """InfoConversationReply unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoConversationReply(self):
        """Test InfoConversationReply"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoConversationReply()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
