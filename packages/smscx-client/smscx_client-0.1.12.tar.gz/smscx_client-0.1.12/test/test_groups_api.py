import unittest

import smscx_client
from smscx_client.api.groups_api import GroupsApi  # noqa: E501


class TestGroupsApi(unittest.TestCase):
    """GroupsApi unit test stubs"""

    def setUp(self):
        self.api = GroupsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_contacts_to_group(self):
        """Test case for add_contacts_to_group

        Add contacts to group  # noqa: E501
        """
        pass

    def test_create_group(self):
        """Test case for create_group

        Create new group  # noqa: E501
        """
        pass

    def test_delete_contact_from_group(self):
        """Test case for delete_contact_from_group

        Delete contact from group  # noqa: E501
        """
        pass

    def test_delete_group(self):
        """Test case for delete_group

        Delete group  # noqa: E501
        """
        pass

    def test_empty_group(self):
        """Test case for empty_group

        Empty group  # noqa: E501
        """
        pass

    def test_export_group_to_csv(self):
        """Test case for export_group_to_csv

        Export group to CSV  # noqa: E501
        """
        pass

    def test_export_group_to_xlsx(self):
        """Test case for export_group_to_xlsx

        Export group to XLSX  # noqa: E501
        """
        pass

    def test_get_group_details(self):
        """Test case for get_group_details

        Get group details  # noqa: E501
        """
        pass

    def test_get_groups_list(self):
        """Test case for get_groups_list

        Get list of groups  # noqa: E501
        """
        pass

    def test_update_contact_from_group(self):
        """Test case for update_contact_from_group

        Update contact from group  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
