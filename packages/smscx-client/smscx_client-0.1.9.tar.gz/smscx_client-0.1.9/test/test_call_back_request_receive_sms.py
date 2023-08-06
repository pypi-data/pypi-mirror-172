import sys
import unittest

import smscx_client
from smscx_client.model.data_receive_sms import DataReceiveSms
globals()['DataReceiveSms'] = DataReceiveSms
from smscx_client.model.call_back_request_receive_sms import CallBackRequestReceiveSms


class TestCallBackRequestReceiveSms(unittest.TestCase):
    """CallBackRequestReceiveSms unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCallBackRequestReceiveSms(self):
        """Test CallBackRequestReceiveSms"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CallBackRequestReceiveSms()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
