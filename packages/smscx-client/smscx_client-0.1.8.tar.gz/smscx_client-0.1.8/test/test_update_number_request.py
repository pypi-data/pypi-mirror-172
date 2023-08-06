import sys
import unittest

import smscx_client
from smscx_client.model.custom_fields_obj import CustomFieldsObj
globals()['CustomFieldsObj'] = CustomFieldsObj
from smscx_client.model.update_number_request import UpdateNumberRequest


class TestUpdateNumberRequest(unittest.TestCase):
    """UpdateNumberRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUpdateNumberRequest(self):
        """Test UpdateNumberRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = UpdateNumberRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
