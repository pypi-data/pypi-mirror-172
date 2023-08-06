import sys
import unittest

import smscx_client
from smscx_client.model.custom_fields import CustomFields
globals()['CustomFields'] = CustomFields
from smscx_client.model.send_viber_message_request import SendViberMessageRequest


class TestSendViberMessageRequest(unittest.TestCase):
    """SendViberMessageRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSendViberMessageRequest(self):
        """Test SendViberMessageRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SendViberMessageRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
