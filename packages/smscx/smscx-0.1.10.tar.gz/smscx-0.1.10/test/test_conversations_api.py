import unittest

import smscx_client
from smscx_client.api.conversations_api import ConversationsApi  # noqa: E501


class TestConversationsApi(unittest.TestCase):
    """ConversationsApi unit test stubs"""

    def setUp(self):
        self.api = ConversationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_conversation(self):
        """Test case for get_conversation

        Get conversation  # noqa: E501
        """
        pass

    def test_get_converstions_list(self):
        """Test case for get_converstions_list

        Get conversations list  # noqa: E501
        """
        pass

    def test_mark_conversation_as_read(self):
        """Test case for mark_conversation_as_read

        Mark conversation as read  # noqa: E501
        """
        pass

    def test_send_conversation_reply_sms(self):
        """Test case for send_conversation_reply_sms

        Send conversation reply via SMS  # noqa: E501
        """
        pass

    def test_send_conversation_reply_viber(self):
        """Test case for send_conversation_reply_viber

        Send conversation reply via Viber  # noqa: E501
        """
        pass

    def test_send_conversation_reply_whatsapp(self):
        """Test case for send_conversation_reply_whatsapp

        Send conversation reply via Whatsapp  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
