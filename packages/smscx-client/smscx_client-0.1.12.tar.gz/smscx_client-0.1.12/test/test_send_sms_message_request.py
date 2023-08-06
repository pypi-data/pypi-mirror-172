import sys
import unittest

import smscx_client
from smscx_client.model.transliteration import Transliteration
globals()['Transliteration'] = Transliteration
from smscx_client.model.send_sms_message_request import SendSmsMessageRequest


class TestSendSmsMessageRequest(unittest.TestCase):
    """SendSmsMessageRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendSmsMessageRequest(self):
        """Test SendSmsMessageRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendSmsMessageRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
