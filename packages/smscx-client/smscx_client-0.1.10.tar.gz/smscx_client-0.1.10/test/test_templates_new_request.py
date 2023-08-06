import sys
import unittest

import smscx_client
from smscx_client.model.rich_media import RichMedia
globals()['RichMedia'] = RichMedia
from smscx_client.model.templates_new_request import TemplatesNewRequest


class TestTemplatesNewRequest(unittest.TestCase):
    """TemplatesNewRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTemplatesNewRequest(self):
        """Test TemplatesNewRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TemplatesNewRequest()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
