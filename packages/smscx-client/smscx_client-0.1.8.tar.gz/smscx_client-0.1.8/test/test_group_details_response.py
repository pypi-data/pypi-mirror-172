import sys
import unittest

import smscx_client
from smscx_client.model.data_groups_details import DataGroupsDetails
from smscx_client.model.info_groups import InfoGroups
from smscx_client.model.paging import Paging
globals()['DataGroupsDetails'] = DataGroupsDetails
globals()['InfoGroups'] = InfoGroups
globals()['Paging'] = Paging
from smscx_client.model.group_details_response import GroupDetailsResponse


class TestGroupDetailsResponse(unittest.TestCase):
    """GroupDetailsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGroupDetailsResponse(self):
        """Test GroupDetailsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GroupDetailsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
