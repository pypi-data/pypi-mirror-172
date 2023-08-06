import sys
import unittest

import smscx_client
from smscx_client.model.data_dlr_update import DataDlrUpdate
globals()['DataDlrUpdate'] = DataDlrUpdate
from smscx_client.model.call_back_request_dlr_update import CallBackRequestDlrUpdate


class TestCallBackRequestDlrUpdate(unittest.TestCase):
    """CallBackRequestDlrUpdate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCallBackRequestDlrUpdate(self):
        """Test CallBackRequestDlrUpdate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CallBackRequestDlrUpdate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
