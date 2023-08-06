import sys
import unittest

import smscx_client
from smscx_client.model.quiet_hours import QuietHours
globals()['QuietHours'] = QuietHours
from smscx_client.model.whatsapp import Whatsapp


class TestWhatsapp(unittest.TestCase):
    """Whatsapp unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testWhatsapp(self):
        """Test Whatsapp"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Whatsapp()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
