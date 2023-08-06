import sys
import unittest

import smscx_client
from smscx_client.model.original_text import OriginalText
from smscx_client.model.replaced_text import ReplacedText
globals()['OriginalText'] = OriginalText
globals()['ReplacedText'] = ReplacedText
from smscx_client.model.text import Text


class TestText(unittest.TestCase):
    """Text unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testText(self):
        """Test Text"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Text()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
