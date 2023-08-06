import sys
import unittest

import smscx_client
from smscx_client.model.data_viber import DataViber
from smscx_client.model.info_conversation_reply import InfoConversationReply
globals()['DataViber'] = DataViber
globals()['InfoConversationReply'] = InfoConversationReply
from smscx_client.model.conversation_reply_whatsapp_response import ConversationReplyWhatsappResponse


class TestConversationReplyWhatsappResponse(unittest.TestCase):
    """ConversationReplyWhatsappResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConversationReplyWhatsappResponse(self):
        """Test ConversationReplyWhatsappResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ConversationReplyWhatsappResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
