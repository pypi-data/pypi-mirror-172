import sys
import unittest

import smscx_client
from smscx_client.model.data_otp import DataOtp
globals()['DataOtp'] = DataOtp
from smscx_client.model.call_back_request_otp_update import CallBackRequestOtpUpdate


class TestCallBackRequestOtpUpdate(unittest.TestCase):
    """CallBackRequestOtpUpdate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCallBackRequestOtpUpdate(self):
        """Test CallBackRequestOtpUpdate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CallBackRequestOtpUpdate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
