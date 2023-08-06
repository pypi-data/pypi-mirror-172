import unittest

import smscx_client
from smscx_client.api.otp_api import OtpApi  # noqa: E501


class TestOtpApi(unittest.TestCase):
    """OtpApi unit test stubs"""

    def setUp(self):
        self.api = OtpApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_cancel_otp(self):
        """Test case for cancel_otp

        Cancel OTP  # noqa: E501
        """
        pass

    def test_get_otp_status(self):
        """Test case for get_otp_status

        Get OTP status  # noqa: E501
        """
        pass

    def test_new_otp(self):
        """Test case for new_otp

        New OTP  # noqa: E501
        """
        pass

    def test_verify_otp(self):
        """Test case for verify_otp

        Verify OTP  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
