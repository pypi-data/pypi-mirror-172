import sys
import unittest

import smscx_client
from smscx_client.model.info_new_group import InfoNewGroup
globals()['InfoNewGroup'] = InfoNewGroup
from smscx_client.model.new_group_response import NewGroupResponse


class TestNewGroupResponse(unittest.TestCase):
    """NewGroupResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNewGroupResponse(self):
        """Test NewGroupResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = NewGroupResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
