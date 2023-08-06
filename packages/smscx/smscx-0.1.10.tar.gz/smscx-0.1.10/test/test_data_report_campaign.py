import sys
import unittest

import smscx_client
from smscx_client.model.text_analysis import TextAnalysis
globals()['TextAnalysis'] = TextAnalysis
from smscx_client.model.data_report_campaign import DataReportCampaign


class TestDataReportCampaign(unittest.TestCase):
    """DataReportCampaign unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataReportCampaign(self):
        """Test DataReportCampaign"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataReportCampaign()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
