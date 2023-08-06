import sys
import unittest

import smscx_client
from smscx_client.model.custom_fields_obj import CustomFieldsObj
globals()['CustomFieldsObj'] = CustomFieldsObj
from smscx_client.model.group_add_custom_fields import GroupAddCustomFields


class TestGroupAddCustomFields(unittest.TestCase):
    """GroupAddCustomFields unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGroupAddCustomFields(self):
        """Test GroupAddCustomFields"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GroupAddCustomFields()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
