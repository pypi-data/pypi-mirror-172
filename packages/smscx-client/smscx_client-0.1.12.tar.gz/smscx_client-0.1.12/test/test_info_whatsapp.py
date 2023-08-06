import sys
import unittest

import smscx_client
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
from smscx_client.model.info_whatsapp import InfoWhatsapp


class TestInfoWhatsapp(unittest.TestCase):
    """InfoWhatsapp unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoWhatsapp(self):
        """Test InfoWhatsapp"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoWhatsapp()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
