import sys
import unittest

import smscx_client
from smscx_client.model.info_id import InfoId
globals()['InfoId'] = InfoId
from smscx_client.model.shortlink_update_response import ShortlinkUpdateResponse


class TestShortlinkUpdateResponse(unittest.TestCase):
    """ShortlinkUpdateResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testShortlinkUpdateResponse(self):
        """Test ShortlinkUpdateResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ShortlinkUpdateResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
