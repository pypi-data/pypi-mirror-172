import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
globals()['Error'] = Error
from smscx_client.model.model403_no_coverage import Model403NoCoverage


class TestModel403NoCoverage(unittest.TestCase):
    """Model403NoCoverage unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel403NoCoverage(self):
        """Test Model403NoCoverage"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Model403NoCoverage()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
