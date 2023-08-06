import sys
import unittest

import smscx_client
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
from smscx_client.model.info_groups_add_contacts_response import InfoGroupsAddContactsResponse


class TestInfoGroupsAddContactsResponse(unittest.TestCase):
    """InfoGroupsAddContactsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoGroupsAddContactsResponse(self):
        """Test InfoGroupsAddContactsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoGroupsAddContactsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
