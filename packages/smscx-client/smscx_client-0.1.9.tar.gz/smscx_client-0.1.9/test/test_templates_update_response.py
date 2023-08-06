import sys
import unittest

import smscx_client
from smscx_client.model.info_template_update import InfoTemplateUpdate
globals()['InfoTemplateUpdate'] = InfoTemplateUpdate
from smscx_client.model.templates_update_response import TemplatesUpdateResponse


class TestTemplatesUpdateResponse(unittest.TestCase):
    """TemplatesUpdateResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTemplatesUpdateResponse(self):
        """Test TemplatesUpdateResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TemplatesUpdateResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
