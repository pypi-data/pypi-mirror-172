import sys
import unittest

import smscx_client
from smscx_client.model.data_report_campaign import DataReportCampaign
from smscx_client.model.info_report_campaign import InfoReportCampaign
from smscx_client.model.paging import Paging
globals()['DataReportCampaign'] = DataReportCampaign
globals()['InfoReportCampaign'] = InfoReportCampaign
globals()['Paging'] = Paging
from smscx_client.model.reports_campaign_response import ReportsCampaignResponse


class TestReportsCampaignResponse(unittest.TestCase):
    """ReportsCampaignResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReportsCampaignResponse(self):
        """Test ReportsCampaignResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ReportsCampaignResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
