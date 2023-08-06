import sys
import unittest

import smscx_client
from smscx_client.model.strategy import Strategy
globals()['Strategy'] = Strategy
from smscx_client.model.send_multichannel_message_request import SendMultichannelMessageRequest


class TestSendMultichannelMessageRequest(unittest.TestCase):
    """SendMultichannelMessageRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendMultichannelMessageRequest(self):
        """Test SendMultichannelMessageRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendMultichannelMessageRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
