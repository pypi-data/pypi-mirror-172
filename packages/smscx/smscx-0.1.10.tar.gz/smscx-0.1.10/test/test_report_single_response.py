import sys
import unittest

import smscx_client
from smscx_client.model.data_report_campaign import DataReportCampaign
globals()['DataReportCampaign'] = DataReportCampaign
from smscx_client.model.report_single_response import ReportSingleResponse


class TestReportSingleResponse(unittest.TestCase):
    """ReportSingleResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReportSingleResponse(self):
        """Test ReportSingleResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ReportSingleResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
