import sys
import unittest

import smscx_client
from smscx_client.model.data_shortlink_hit import DataShortlinkHit
globals()['DataShortlinkHit'] = DataShortlinkHit
from smscx_client.model.call_back_request_shortlink_hit import CallBackRequestShortlinkHit


class TestCallBackRequestShortlinkHit(unittest.TestCase):
    """CallBackRequestShortlinkHit unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCallBackRequestShortlinkHit(self):
        """Test CallBackRequestShortlinkHit"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CallBackRequestShortlinkHit()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
