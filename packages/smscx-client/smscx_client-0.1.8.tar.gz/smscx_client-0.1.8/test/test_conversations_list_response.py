import sys
import unittest

import smscx_client
from smscx_client.model.data_conversations import DataConversations
globals()['DataConversations'] = DataConversations
from smscx_client.model.conversations_list_response import ConversationsListResponse


class TestConversationsListResponse(unittest.TestCase):
    """ConversationsListResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConversationsListResponse(self):
        """Test ConversationsListResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ConversationsListResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
