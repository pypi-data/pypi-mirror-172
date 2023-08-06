import sys
import unittest

import smscx_client
from smscx_client.model.info_groups_contact_deleted import InfoGroupsContactDeleted
globals()['InfoGroupsContactDeleted'] = InfoGroupsContactDeleted
from smscx_client.model.delete_contact import DeleteContact


class TestDeleteContact(unittest.TestCase):
    """DeleteContact unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDeleteContact(self):
        """Test DeleteContact"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DeleteContact()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
