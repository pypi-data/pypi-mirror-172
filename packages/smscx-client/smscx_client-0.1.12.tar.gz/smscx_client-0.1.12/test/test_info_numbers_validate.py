import sys
import unittest

import smscx_client
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
from smscx_client.model.info_numbers_validate import InfoNumbersValidate


class TestInfoNumbersValidate(unittest.TestCase):
    """InfoNumbersValidate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoNumbersValidate(self):
        """Test InfoNumbersValidate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoNumbersValidate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
