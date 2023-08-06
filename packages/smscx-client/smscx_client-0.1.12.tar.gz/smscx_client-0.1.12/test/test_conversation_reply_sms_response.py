import sys
import unittest

import smscx_client
from smscx_client.model.data_conversation_reply import DataConversationReply
from smscx_client.model.info_conversation_reply import InfoConversationReply
globals()['DataConversationReply'] = DataConversationReply
globals()['InfoConversationReply'] = InfoConversationReply
from smscx_client.model.conversation_reply_sms_response import ConversationReplySmsResponse


class TestConversationReplySmsResponse(unittest.TestCase):
    """ConversationReplySmsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConversationReplySmsResponse(self):
        """Test ConversationReplySmsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ConversationReplySmsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
