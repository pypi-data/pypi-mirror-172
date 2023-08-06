import sys
import unittest

import smscx_client
from smscx_client.model.data_sms import DataSms
from smscx_client.model.info_campaign import InfoCampaign
globals()['DataSms'] = DataSms
globals()['InfoCampaign'] = InfoCampaign
from smscx_client.model.send_sms_campaign_response import SendSmsCampaignResponse


class TestSendSmsCampaignResponse(unittest.TestCase):
    """SendSmsCampaignResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendSmsCampaignResponse(self):
        """Test SendSmsCampaignResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendSmsCampaignResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
