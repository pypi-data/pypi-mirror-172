import sys
import unittest

import smscx_client
from smscx_client.model.info_delete_scheduled_campaign import InfoDeleteScheduledCampaign
globals()['InfoDeleteScheduledCampaign'] = InfoDeleteScheduledCampaign
from smscx_client.model.delete_scheduled_campaign import DeleteScheduledCampaign


class TestDeleteScheduledCampaign(unittest.TestCase):
    """DeleteScheduledCampaign unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDeleteScheduledCampaign(self):
        """Test DeleteScheduledCampaign"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DeleteScheduledCampaign()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
