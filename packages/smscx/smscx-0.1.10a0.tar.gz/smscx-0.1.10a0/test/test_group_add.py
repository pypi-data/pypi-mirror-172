import sys
import unittest

import smscx_client
from smscx_client.model.group_add_custom_fields import GroupAddCustomFields
globals()['GroupAddCustomFields'] = GroupAddCustomFields
from smscx_client.model.group_add import GroupAdd


class TestGroupAdd(unittest.TestCase):
    """GroupAdd unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGroupAdd(self):
        """Test GroupAdd"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GroupAdd()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
