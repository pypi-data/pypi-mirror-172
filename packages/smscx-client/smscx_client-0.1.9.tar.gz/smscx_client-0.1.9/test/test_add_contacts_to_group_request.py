import sys
import unittest

import smscx_client
from smscx_client.model.add_contacts_to_group_request import AddContactsToGroupRequest
from smscx_client.model.add_contacts_to_group_with_fields_request import AddContactsToGroupWithFieldsRequest
from smscx_client.model.group_add import GroupAdd
globals()['AddContactsToGroupRequest'] = AddContactsToGroupRequest
globals()['AddContactsToGroupWithFieldsRequest'] = AddContactsToGroupWithFieldsRequest
globals()['GroupAdd'] = GroupAdd


class TestAddContactsToGroupRequest(unittest.TestCase):
    """AddContactsToGroupRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAddContactsToGroupRequest(self):
        """Test AddContactsToGroupRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = AddContactsToGroupRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
