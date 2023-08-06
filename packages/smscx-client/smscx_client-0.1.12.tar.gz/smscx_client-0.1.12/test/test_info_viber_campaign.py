import sys
import unittest

import smscx_client
from smscx_client.model.group import Group
from smscx_client.model.phone_numbers_by_country import PhoneNumbersByCountry
globals()['Group'] = Group
globals()['PhoneNumbersByCountry'] = PhoneNumbersByCountry
from smscx_client.model.info_viber_campaign import InfoViberCampaign


class TestInfoViberCampaign(unittest.TestCase):
    """InfoViberCampaign unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoViberCampaign(self):
        """Test InfoViberCampaign"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoViberCampaign()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
