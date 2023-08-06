import sys
import unittest

import smscx_client
from smscx_client.model.text_analysis import TextAnalysis
globals()['TextAnalysis'] = TextAnalysis
from smscx_client.model.data_sms import DataSms


class TestDataSms(unittest.TestCase):
    """DataSms unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataSms(self):
        """Test DataSms"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataSms()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
