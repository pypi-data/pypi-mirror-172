import sys
import unittest

import smscx_client
from smscx_client.model.data_numbers_validate import DataNumbersValidate
from smscx_client.model.info_numbers_validate import InfoNumbersValidate
globals()['DataNumbersValidate'] = DataNumbersValidate
globals()['InfoNumbersValidate'] = InfoNumbersValidate
from smscx_client.model.numbers_validate_response import NumbersValidateResponse


class TestNumbersValidateResponse(unittest.TestCase):
    """NumbersValidateResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNumbersValidateResponse(self):
        """Test NumbersValidateResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = NumbersValidateResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
