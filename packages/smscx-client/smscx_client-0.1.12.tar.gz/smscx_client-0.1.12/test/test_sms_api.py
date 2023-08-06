import unittest

import smscx_client
from smscx_client.api.sms_api import SmsApi  # noqa: E501


class TestSmsApi(unittest.TestCase):
    """SmsApi unit test stubs"""

    def setUp(self):
        self.api = SmsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_scheduled_sms(self):
        """Test case for delete_scheduled_sms

        Delete scheduled SMS  # noqa: E501
        """
        pass

    def test_delete_scheduled_sms_campaign(self):
        """Test case for delete_scheduled_sms_campaign

        Delete scheduled SMS campaign  # noqa: E501
        """
        pass

    def test_estimate_sms(self):
        """Test case for estimate_sms

        Estimate new SMS  # noqa: E501
        """
        pass

    def test_estimate_sms_campaign(self):
        """Test case for estimate_sms_campaign

        Estimate SMS campaign  # noqa: E501
        """
        pass

    def test_send_sms(self):
        """Test case for send_sms

        Send SMS  # noqa: E501
        """
        pass

    def test_send_sms_campaign(self):
        """Test case for send_sms_campaign

        Send SMS campaign  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
