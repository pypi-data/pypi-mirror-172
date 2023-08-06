import sys
import unittest

import smscx_client
from smscx_client.model.data_viber import DataViber
from smscx_client.model.info_conversation_reply import InfoConversationReply
globals()['DataViber'] = DataViber
globals()['InfoConversationReply'] = InfoConversationReply
from smscx_client.model.conversation_reply_viber_respone import ConversationReplyViberRespone


class TestConversationReplyViberRespone(unittest.TestCase):
    """ConversationReplyViberRespone unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConversationReplyViberRespone(self):
        """Test ConversationReplyViberRespone"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ConversationReplyViberRespone()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
