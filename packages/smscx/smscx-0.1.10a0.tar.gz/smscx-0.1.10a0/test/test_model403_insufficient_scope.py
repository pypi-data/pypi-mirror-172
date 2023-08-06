import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
globals()['Error'] = Error
from smscx_client.model.model403_insufficient_scope import Model403InsufficientScope


class TestModel403InsufficientScope(unittest.TestCase):
    """Model403InsufficientScope unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel403InsufficientScope(self):
        """Test Model403InsufficientScope"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Model403InsufficientScope()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
