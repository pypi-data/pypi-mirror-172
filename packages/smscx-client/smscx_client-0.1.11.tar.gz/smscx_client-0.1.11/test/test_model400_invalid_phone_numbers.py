import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
globals()['Error'] = Error
from smscx_client.model.model400_invalid_phone_numbers import Model400InvalidPhoneNumbers


class TestModel400InvalidPhoneNumbers(unittest.TestCase):
    """Model400InvalidPhoneNumbers unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel400InvalidPhoneNumbers(self):
        """Test Model400InvalidPhoneNumbers"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Model400InvalidPhoneNumbers()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
