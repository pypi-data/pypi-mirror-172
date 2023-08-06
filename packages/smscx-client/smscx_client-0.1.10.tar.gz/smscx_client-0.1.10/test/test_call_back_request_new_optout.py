import sys
import unittest

import smscx_client
from smscx_client.model.data_new_optout import DataNewOptout
globals()['DataNewOptout'] = DataNewOptout
from smscx_client.model.call_back_request_new_optout import CallBackRequestNewOptout


class TestCallBackRequestNewOptout(unittest.TestCase):
    """CallBackRequestNewOptout unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCallBackRequestNewOptout(self):
        """Test CallBackRequestNewOptout"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CallBackRequestNewOptout()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
