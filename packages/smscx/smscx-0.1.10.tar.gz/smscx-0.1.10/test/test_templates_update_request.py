import sys
import unittest

import smscx_client
from smscx_client.model.rich_media import RichMedia
globals()['RichMedia'] = RichMedia
from smscx_client.model.templates_update_request import TemplatesUpdateRequest


class TestTemplatesUpdateRequest(unittest.TestCase):
    """TemplatesUpdateRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTemplatesUpdateRequest(self):
        """Test TemplatesUpdateRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TemplatesUpdateRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
