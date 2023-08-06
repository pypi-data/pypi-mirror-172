import sys
import unittest

import smscx_client
from smscx_client.model.info_originator import InfoOriginator
globals()['InfoOriginator'] = InfoOriginator
from smscx_client.model.originator_new_response import OriginatorNewResponse


class TestOriginatorNewResponse(unittest.TestCase):
    """OriginatorNewResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOriginatorNewResponse(self):
        """Test OriginatorNewResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = OriginatorNewResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
