import sys
import unittest

import smscx_client
from smscx_client.model.two_way import TwoWay
globals()['TwoWay'] = TwoWay
from smscx_client.model.data_originators_list import DataOriginatorsList


class TestDataOriginatorsList(unittest.TestCase):
    """DataOriginatorsList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataOriginatorsList(self):
        """Test DataOriginatorsList"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataOriginatorsList()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
