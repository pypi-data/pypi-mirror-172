import sys
import unittest

import smscx_client
from smscx_client.model.settings import Settings
globals()['Settings'] = Settings
from smscx_client.model.application_settings_response import ApplicationSettingsResponse


class TestApplicationSettingsResponse(unittest.TestCase):
    """ApplicationSettingsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testApplicationSettingsResponse(self):
        """Test ApplicationSettingsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ApplicationSettingsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
