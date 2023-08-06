import sys
import unittest

import smscx_client
from smscx_client.model.info_id import InfoId
globals()['InfoId'] = InfoId
from smscx_client.model.conversation_read_response import ConversationReadResponse


class TestConversationReadResponse(unittest.TestCase):
    """ConversationReadResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConversationReadResponse(self):
        """Test ConversationReadResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ConversationReadResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
