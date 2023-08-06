import sys
import unittest

import smscx_client
from smscx_client.model.info_id import InfoId
globals()['InfoId'] = InfoId
from smscx_client.model.shortlink_delete_response import ShortlinkDeleteResponse


class TestShortlinkDeleteResponse(unittest.TestCase):
    """ShortlinkDeleteResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testShortlinkDeleteResponse(self):
        """Test ShortlinkDeleteResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ShortlinkDeleteResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
