import sys
import unittest

import smscx_client
from smscx_client.model.text_analysis import TextAnalysis
globals()['TextAnalysis'] = TextAnalysis
from smscx_client.model.data_conversation_reply import DataConversationReply


class TestDataConversationReply(unittest.TestCase):
    """DataConversationReply unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataConversationReply(self):
        """Test DataConversationReply"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataConversationReply()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
