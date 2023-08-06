import sys
import unittest

import smscx_client
from smscx_client.model.data_shortlink_hit import DataShortlinkHit
globals()['DataShortlinkHit'] = DataShortlinkHit
from smscx_client.model.call_back_request_attachment_hit import CallBackRequestAttachmentHit


class TestCallBackRequestAttachmentHit(unittest.TestCase):
    """CallBackRequestAttachmentHit unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCallBackRequestAttachmentHit(self):
        """Test CallBackRequestAttachmentHit"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CallBackRequestAttachmentHit()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
