import sys
import unittest

import smscx_client
from smscx_client.model.data_shortlink_detail import DataShortlinkDetail
from smscx_client.model.info_shortlink_detail import InfoShortlinkDetail
from smscx_client.model.paging import Paging
globals()['DataShortlinkDetail'] = DataShortlinkDetail
globals()['InfoShortlinkDetail'] = InfoShortlinkDetail
globals()['Paging'] = Paging
from smscx_client.model.shortlink_details_response import ShortlinkDetailsResponse


class TestShortlinkDetailsResponse(unittest.TestCase):
    """ShortlinkDetailsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testShortlinkDetailsResponse(self):
        """Test ShortlinkDetailsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ShortlinkDetailsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
