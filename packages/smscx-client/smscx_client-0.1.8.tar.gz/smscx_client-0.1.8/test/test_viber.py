import sys
import unittest

import smscx_client
from smscx_client.model.quiet_hours import QuietHours
globals()['QuietHours'] = QuietHours
from smscx_client.model.viber import Viber


class TestViber(unittest.TestCase):
    """Viber unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testViber(self):
        """Test Viber"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Viber()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
