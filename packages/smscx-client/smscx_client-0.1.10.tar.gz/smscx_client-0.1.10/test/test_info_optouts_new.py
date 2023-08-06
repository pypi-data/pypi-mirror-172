import sys
import unittest

import smscx_client
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
from smscx_client.model.info_optouts_new import InfoOptoutsNew


class TestInfoOptoutsNew(unittest.TestCase):
    """InfoOptoutsNew unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoOptoutsNew(self):
        """Test InfoOptoutsNew"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoOptoutsNew()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
