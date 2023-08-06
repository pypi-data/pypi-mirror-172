import sys
import unittest

import smscx_client
from smscx_client.model.data_shortlink_detail import DataShortlinkDetail
from smscx_client.model.info_attachment import InfoAttachment
from smscx_client.model.paging import Paging
globals()['DataShortlinkDetail'] = DataShortlinkDetail
globals()['InfoAttachment'] = InfoAttachment
globals()['Paging'] = Paging
from smscx_client.model.attachment_details_response import AttachmentDetailsResponse


class TestAttachmentDetailsResponse(unittest.TestCase):
    """AttachmentDetailsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAttachmentDetailsResponse(self):
        """Test AttachmentDetailsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = AttachmentDetailsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
