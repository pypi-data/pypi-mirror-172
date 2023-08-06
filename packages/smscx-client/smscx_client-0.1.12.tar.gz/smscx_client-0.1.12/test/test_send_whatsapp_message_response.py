import sys
import unittest

import smscx_client
from smscx_client.model.data_whatsapp import DataWhatsapp
from smscx_client.model.info_whatsapp import InfoWhatsapp
globals()['DataWhatsapp'] = DataWhatsapp
globals()['InfoWhatsapp'] = InfoWhatsapp
from smscx_client.model.send_whatsapp_message_response import SendWhatsappMessageResponse


class TestSendWhatsappMessageResponse(unittest.TestCase):
    """SendWhatsappMessageResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendWhatsappMessageResponse(self):
        """Test SendWhatsappMessageResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendWhatsappMessageResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
