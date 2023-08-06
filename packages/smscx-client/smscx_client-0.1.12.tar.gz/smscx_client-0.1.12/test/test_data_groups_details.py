import sys
import unittest

import smscx_client
from smscx_client.model.custom_fields_obj import CustomFieldsObj
globals()['CustomFieldsObj'] = CustomFieldsObj
from smscx_client.model.data_groups_details import DataGroupsDetails


class TestDataGroupsDetails(unittest.TestCase):
    """DataGroupsDetails unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataGroupsDetails(self):
        """Test DataGroupsDetails"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataGroupsDetails()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
