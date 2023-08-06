import sys
import unittest

import smscx_client
from smscx_client.model.data_conversation import DataConversation
from smscx_client.model.info_conversation import InfoConversation
globals()['DataConversation'] = DataConversation
globals()['InfoConversation'] = InfoConversation
from smscx_client.model.conversation_details_response import ConversationDetailsResponse


class TestConversationDetailsResponse(unittest.TestCase):
    """ConversationDetailsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConversationDetailsResponse(self):
        """Test ConversationDetailsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ConversationDetailsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
