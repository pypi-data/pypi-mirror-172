import sys
import unittest

import smscx_client
from smscx_client.model.info_otp import InfoOtp
globals()['InfoOtp'] = InfoOtp
from smscx_client.model.cancel_otp_response import CancelOtpResponse


class TestCancelOtpResponse(unittest.TestCase):
    """CancelOtpResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCancelOtpResponse(self):
        """Test CancelOtpResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CancelOtpResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
