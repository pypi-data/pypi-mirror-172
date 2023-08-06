import sys
import unittest

import smscx_client
from smscx_client.model.info_group import InfoGroup
globals()['InfoGroup'] = InfoGroup
from smscx_client.model.group_response import GroupResponse


class TestGroupResponse(unittest.TestCase):
    """GroupResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGroupResponse(self):
        """Test GroupResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GroupResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
