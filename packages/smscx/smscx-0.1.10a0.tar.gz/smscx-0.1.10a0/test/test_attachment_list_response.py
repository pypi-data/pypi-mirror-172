import sys
import unittest

import smscx_client
from smscx_client.model.data_attachment import DataAttachment
globals()['DataAttachment'] = DataAttachment
from smscx_client.model.attachment_list_response import AttachmentListResponse


class TestAttachmentListResponse(unittest.TestCase):
    """AttachmentListResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAttachmentListResponse(self):
        """Test AttachmentListResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = AttachmentListResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
