import sys
import unittest

import smscx_client
from smscx_client.model.info_shortlink_new import InfoShortlinkNew
globals()['InfoShortlinkNew'] = InfoShortlinkNew
from smscx_client.model.shortlink_new_response import ShortlinkNewResponse


class TestShortlinkNewResponse(unittest.TestCase):
    """ShortlinkNewResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testShortlinkNewResponse(self):
        """Test ShortlinkNewResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ShortlinkNewResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
