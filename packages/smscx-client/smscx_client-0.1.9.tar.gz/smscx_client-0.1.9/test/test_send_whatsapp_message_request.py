import sys
import unittest

import smscx_client
from smscx_client.model.custom_fields import CustomFields
globals()['CustomFields'] = CustomFields
from smscx_client.model.send_whatsapp_message_request import SendWhatsappMessageRequest


class TestSendWhatsappMessageRequest(unittest.TestCase):
    """SendWhatsappMessageRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendWhatsappMessageRequest(self):
        """Test SendWhatsappMessageRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendWhatsappMessageRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
