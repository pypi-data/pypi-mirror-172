import sys
import unittest

import smscx_client
from smscx_client.model.strategy import Strategy
globals()['Strategy'] = Strategy
from smscx_client.model.send_multichannel_message_request_estimate import SendMultichannelMessageRequestEstimate


class TestSendMultichannelMessageRequestEstimate(unittest.TestCase):
    """SendMultichannelMessageRequestEstimate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendMultichannelMessageRequestEstimate(self):
        """Test SendMultichannelMessageRequestEstimate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendMultichannelMessageRequestEstimate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
