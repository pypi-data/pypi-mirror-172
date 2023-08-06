import sys
import unittest

import smscx_client
from smscx_client.model.info_delete_scheduled_msg import InfoDeleteScheduledMsg
globals()['InfoDeleteScheduledMsg'] = InfoDeleteScheduledMsg
from smscx_client.model.delete_scheduled_msg import DeleteScheduledMsg


class TestDeleteScheduledMsg(unittest.TestCase):
    """DeleteScheduledMsg unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDeleteScheduledMsg(self):
        """Test DeleteScheduledMsg"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DeleteScheduledMsg()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
