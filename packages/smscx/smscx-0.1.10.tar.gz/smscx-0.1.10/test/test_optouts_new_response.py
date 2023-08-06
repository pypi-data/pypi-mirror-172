import sys
import unittest

import smscx_client
from smscx_client.model.info_optouts_new import InfoOptoutsNew
globals()['InfoOptoutsNew'] = InfoOptoutsNew
from smscx_client.model.optouts_new_response import OptoutsNewResponse


class TestOptoutsNewResponse(unittest.TestCase):
    """OptoutsNewResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOptoutsNewResponse(self):
        """Test OptoutsNewResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = OptoutsNewResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
