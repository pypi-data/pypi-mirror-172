import sys
import unittest

import smscx_client
from smscx_client.model.custom_fields import CustomFields
globals()['CustomFields'] = CustomFields
from smscx_client.model.send_whatsapp_message_request_estimate import SendWhatsappMessageRequestEstimate


class TestSendWhatsappMessageRequestEstimate(unittest.TestCase):
    """SendWhatsappMessageRequestEstimate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendWhatsappMessageRequestEstimate(self):
        """Test SendWhatsappMessageRequestEstimate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendWhatsappMessageRequestEstimate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
