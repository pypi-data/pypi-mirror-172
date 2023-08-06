import sys
import unittest

import smscx_client
from smscx_client.model.info_delete_group import InfoDeleteGroup
globals()['InfoDeleteGroup'] = InfoDeleteGroup
from smscx_client.model.delete_group import DeleteGroup


class TestDeleteGroup(unittest.TestCase):
    """DeleteGroup unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDeleteGroup(self):
        """Test DeleteGroup"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DeleteGroup()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
