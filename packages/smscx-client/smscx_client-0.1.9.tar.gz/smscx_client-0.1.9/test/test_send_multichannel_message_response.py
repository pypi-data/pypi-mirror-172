import sys
import unittest

import smscx_client
from smscx_client.model.data_multichannel import DataMultichannel
from smscx_client.model.info_multichannel import InfoMultichannel
globals()['DataMultichannel'] = DataMultichannel
globals()['InfoMultichannel'] = InfoMultichannel
from smscx_client.model.send_multichannel_message_response import SendMultichannelMessageResponse


class TestSendMultichannelMessageResponse(unittest.TestCase):
    """SendMultichannelMessageResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendMultichannelMessageResponse(self):
        """Test SendMultichannelMessageResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendMultichannelMessageResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
