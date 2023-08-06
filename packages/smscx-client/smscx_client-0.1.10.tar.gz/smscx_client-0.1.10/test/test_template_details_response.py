import sys
import unittest

import smscx_client
from smscx_client.model.data_template import DataTemplate
globals()['DataTemplate'] = DataTemplate
from smscx_client.model.template_details_response import TemplateDetailsResponse


class TestTemplateDetailsResponse(unittest.TestCase):
    """TemplateDetailsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTemplateDetailsResponse(self):
        """Test TemplateDetailsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TemplateDetailsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
