import sys
import unittest

import smscx_client
from smscx_client.model.text import Text
globals()['Text'] = Text
from smscx_client.model.transliteration_analysis import TransliterationAnalysis


class TestTransliterationAnalysis(unittest.TestCase):
    """TransliterationAnalysis unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTransliterationAnalysis(self):
        """Test TransliterationAnalysis"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TransliterationAnalysis()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
