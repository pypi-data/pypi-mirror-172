import sys
import unittest

import smscx_client
from smscx_client.model.data_receive_sms import DataReceiveSms
from smscx_client.model.info_inbound_sms import InfoInboundSms
from smscx_client.model.paging import Paging
globals()['DataReceiveSms'] = DataReceiveSms
globals()['InfoInboundSms'] = InfoInboundSms
globals()['Paging'] = Paging
from smscx_client.model.get_inbound_sms_response import GetInboundSMSResponse


class TestGetInboundSMSResponse(unittest.TestCase):
    """GetInboundSMSResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetInboundSMSResponse(self):
        """Test GetInboundSMSResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GetInboundSMSResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
