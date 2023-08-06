import sys
import unittest

import smscx_client
from smscx_client.model.info_template_update import InfoTemplateUpdate
globals()['InfoTemplateUpdate'] = InfoTemplateUpdate
from smscx_client.model.templates_delete_response import TemplatesDeleteResponse


class TestTemplatesDeleteResponse(unittest.TestCase):
    """TemplatesDeleteResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTemplatesDeleteResponse(self):
        """Test TemplatesDeleteResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TemplatesDeleteResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
