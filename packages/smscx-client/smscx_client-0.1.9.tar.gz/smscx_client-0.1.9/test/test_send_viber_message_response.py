import sys
import unittest

import smscx_client
from smscx_client.model.data_viber import DataViber
from smscx_client.model.info_viber import InfoViber
globals()['DataViber'] = DataViber
globals()['InfoViber'] = InfoViber
from smscx_client.model.send_viber_message_response import SendViberMessageResponse


class TestSendViberMessageResponse(unittest.TestCase):
    """SendViberMessageResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendViberMessageResponse(self):
        """Test SendViberMessageResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendViberMessageResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
