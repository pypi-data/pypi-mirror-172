import sys
import unittest

import smscx_client
from smscx_client.model.info_id import InfoId
globals()['InfoId'] = InfoId
from smscx_client.model.attachment_delete_response import AttachmentDeleteResponse


class TestAttachmentDeleteResponse(unittest.TestCase):
    """AttachmentDeleteResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAttachmentDeleteResponse(self):
        """Test AttachmentDeleteResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = AttachmentDeleteResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
