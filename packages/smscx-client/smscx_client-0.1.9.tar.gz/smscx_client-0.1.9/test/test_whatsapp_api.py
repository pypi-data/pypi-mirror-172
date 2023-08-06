import unittest

import smscx_client
from smscx_client.api.whatsapp_api import WhatsappApi  # noqa: E501


class TestWhatsappApi(unittest.TestCase):
    """WhatsappApi unit test stubs"""

    def setUp(self):
        self.api = WhatsappApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_scheduled_whatsapp_message(self):
        """Test case for delete_scheduled_whatsapp_message

        Delete scheduled Whatsapp message  # noqa: E501
        """
        pass

    def test_estimate_whatsapp_message(self):
        """Test case for estimate_whatsapp_message

        Estimate Whatsapp message  # noqa: E501
        """
        pass

    def test_send_whatsapp_message(self):
        """Test case for send_whatsapp_message

        Send Whatsapp message  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
