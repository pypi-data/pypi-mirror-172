import sys
import unittest

import smscx_client
from smscx_client.model.text_analysis import TextAnalysis
globals()['TextAnalysis'] = TextAnalysis
from smscx_client.model.data_reports import DataReports


class TestDataReports(unittest.TestCase):
    """DataReports unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataReports(self):
        """Test DataReports"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataReports()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
