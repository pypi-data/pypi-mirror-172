import sys
import unittest

import smscx_client
from smscx_client.model.pricing_sms_response import PricingSmsResponse
from smscx_client.model.pricing_viber_whatsapp_response import PricingViberWhatsappResponse
from smscx_client.model.viber_whatsapp_pricing import ViberWhatsappPricing
globals()['PricingSmsResponse'] = PricingSmsResponse
globals()['PricingViberWhatsappResponse'] = PricingViberWhatsappResponse
globals()['ViberWhatsappPricing'] = ViberWhatsappPricing
from smscx_client.model.get_channel_pricing200_response import GetChannelPricing200Response


class TestGetChannelPricing200Response(unittest.TestCase):
    """GetChannelPricing200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetChannelPricing200Response(self):
        """Test GetChannelPricing200Response"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GetChannelPricing200Response()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
