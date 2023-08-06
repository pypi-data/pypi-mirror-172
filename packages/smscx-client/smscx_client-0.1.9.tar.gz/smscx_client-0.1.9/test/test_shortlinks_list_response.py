import sys
import unittest

import smscx_client
from smscx_client.model.data_shortlink_list import DataShortlinkList
globals()['DataShortlinkList'] = DataShortlinkList
from smscx_client.model.shortlinks_list_response import ShortlinksListResponse


class TestShortlinksListResponse(unittest.TestCase):
    """ShortlinksListResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testShortlinksListResponse(self):
        """Test ShortlinksListResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ShortlinksListResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
