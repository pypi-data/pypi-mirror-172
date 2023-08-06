import sys
import unittest

import smscx_client
from smscx_client.model.data_sms import DataSms
from smscx_client.model.info import Info
globals()['DataSms'] = DataSms
globals()['Info'] = Info
from smscx_client.model.send_sms_message_response import SendSmsMessageResponse


class TestSendSmsMessageResponse(unittest.TestCase):
    """SendSmsMessageResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendSmsMessageResponse(self):
        """Test SendSmsMessageResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendSmsMessageResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
