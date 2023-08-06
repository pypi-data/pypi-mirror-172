import sys
import unittest

import smscx_client
from smscx_client.model.info_template import InfoTemplate
globals()['InfoTemplate'] = InfoTemplate
from smscx_client.model.templates_new_response import TemplatesNewResponse


class TestTemplatesNewResponse(unittest.TestCase):
    """TemplatesNewResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTemplatesNewResponse(self):
        """Test TemplatesNewResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TemplatesNewResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
