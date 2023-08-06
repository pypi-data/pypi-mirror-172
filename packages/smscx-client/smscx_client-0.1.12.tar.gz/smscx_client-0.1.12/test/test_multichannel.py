import sys
import unittest

import smscx_client
from smscx_client.model.quiet_hours import QuietHours
globals()['QuietHours'] = QuietHours
from smscx_client.model.multichannel import Multichannel


class TestMultichannel(unittest.TestCase):
    """Multichannel unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testMultichannel(self):
        """Test Multichannel"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Multichannel()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
