import sys
import unittest

import smscx_client
from smscx_client.model.transliteration import Transliteration
globals()['Transliteration'] = Transliteration
from smscx_client.model.send_sms_request_estimate import SendSmsRequestEstimate


class TestSendSmsRequestEstimate(unittest.TestCase):
    """SendSmsRequestEstimate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendSmsRequestEstimate(self):
        """Test SendSmsRequestEstimate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendSmsRequestEstimate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
