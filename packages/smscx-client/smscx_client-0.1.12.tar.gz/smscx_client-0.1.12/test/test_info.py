import sys
import unittest

import smscx_client
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
from smscx_client.model.transliteration_analysis import TransliterationAnalysis
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
globals()['TransliterationAnalysis'] = TransliterationAnalysis
from smscx_client.model.info import Info


class TestInfo(unittest.TestCase):
    """Info unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfo(self):
        """Test Info"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Info()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
