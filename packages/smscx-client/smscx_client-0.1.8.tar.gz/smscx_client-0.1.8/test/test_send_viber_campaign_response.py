import sys
import unittest

import smscx_client
from smscx_client.model.data_viber import DataViber
from smscx_client.model.info_viber_campaign import InfoViberCampaign
globals()['DataViber'] = DataViber
globals()['InfoViberCampaign'] = InfoViberCampaign
from smscx_client.model.send_viber_campaign_response import SendViberCampaignResponse


class TestSendViberCampaignResponse(unittest.TestCase):
    """SendViberCampaignResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendViberCampaignResponse(self):
        """Test SendViberCampaignResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendViberCampaignResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
