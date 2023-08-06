import sys
import unittest

import smscx_client
from smscx_client.model.data_templates_list import DataTemplatesList
globals()['DataTemplatesList'] = DataTemplatesList
from smscx_client.model.templates_list_response import TemplatesListResponse


class TestTemplatesListResponse(unittest.TestCase):
    """TemplatesListResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTemplatesListResponse(self):
        """Test TemplatesListResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TemplatesListResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
