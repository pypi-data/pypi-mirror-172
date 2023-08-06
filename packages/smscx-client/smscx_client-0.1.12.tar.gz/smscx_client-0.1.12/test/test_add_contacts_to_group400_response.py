import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
from smscx_client.model.model400_invalid_param_groups import Model400InvalidParamGroups
from smscx_client.model.model400_invalid_phone_numbers import Model400InvalidPhoneNumbers
globals()['Error'] = Error
globals()['Model400InvalidParamGroups'] = Model400InvalidParamGroups
globals()['Model400InvalidPhoneNumbers'] = Model400InvalidPhoneNumbers
from smscx_client.model.add_contacts_to_group400_response import AddContactsToGroup400Response


class TestAddContactsToGroup400Response(unittest.TestCase):
    """AddContactsToGroup400Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAddContactsToGroup400Response(self):
        """Test AddContactsToGroup400Response"""
        # FIXME: construct object with mandatory attributes with example values
        # model = AddContactsToGroup400Response()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
