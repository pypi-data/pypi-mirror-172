import sys
import unittest

import smscx_client
from smscx_client.model.data_number_validate import DataNumberValidate
globals()['DataNumberValidate'] = DataNumberValidate
from smscx_client.model.number_validate_response import NumberValidateResponse


class TestNumberValidateResponse(unittest.TestCase):
    """NumberValidateResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNumberValidateResponse(self):
        """Test NumberValidateResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = NumberValidateResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
