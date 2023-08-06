import sys
import unittest

import smscx_client
from smscx_client.model.data_groups import DataGroups
globals()['DataGroups'] = DataGroups
from smscx_client.model.groups_list import GroupsList


class TestGroupsList(unittest.TestCase):
    """GroupsList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGroupsList(self):
        """Test GroupsList"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GroupsList()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
