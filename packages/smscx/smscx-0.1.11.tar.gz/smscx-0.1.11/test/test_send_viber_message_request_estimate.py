import sys
import unittest

import smscx_client
from smscx_client.model.custom_fields import CustomFields
globals()['CustomFields'] = CustomFields
from smscx_client.model.send_viber_message_request_estimate import SendViberMessageRequestEstimate


class TestSendViberMessageRequestEstimate(unittest.TestCase):
    """SendViberMessageRequestEstimate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendViberMessageRequestEstimate(self):
        """Test SendViberMessageRequestEstimate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendViberMessageRequestEstimate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
