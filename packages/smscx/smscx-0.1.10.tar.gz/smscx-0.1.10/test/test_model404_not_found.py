import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
globals()['Error'] = Error
from smscx_client.model.model404_not_found import Model404NotFound


class TestModel404NotFound(unittest.TestCase):
    """Model404NotFound unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel404NotFound(self):
        """Test Model404NotFound"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Model404NotFound()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
