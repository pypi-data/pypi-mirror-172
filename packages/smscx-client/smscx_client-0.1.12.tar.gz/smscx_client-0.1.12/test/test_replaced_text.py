import sys
import unittest

import smscx_client
from smscx_client.model.characters_replaced import CharactersReplaced
globals()['CharactersReplaced'] = CharactersReplaced
from smscx_client.model.replaced_text import ReplacedText


class TestReplacedText(unittest.TestCase):
    """ReplacedText unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReplacedText(self):
        """Test ReplacedText"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ReplacedText()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
