import sys
import unittest

import smscx_client
from smscx_client.model.quiet_hours import QuietHours
from smscx_client.model.transliteration_app_settings import TransliterationAppSettings
globals()['QuietHours'] = QuietHours
globals()['TransliterationAppSettings'] = TransliterationAppSettings
from smscx_client.model.sms import Sms


class TestSms(unittest.TestCase):
    """Sms unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSms(self):
        """Test Sms"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Sms()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
