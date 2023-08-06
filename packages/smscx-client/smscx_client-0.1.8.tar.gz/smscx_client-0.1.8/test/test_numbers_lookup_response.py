import sys
import unittest

import smscx_client
from smscx_client.model.data_numbers_lookup import DataNumbersLookup
from smscx_client.model.info_numbers_lookup import InfoNumbersLookup
globals()['DataNumbersLookup'] = DataNumbersLookup
globals()['InfoNumbersLookup'] = InfoNumbersLookup
from smscx_client.model.numbers_lookup_response import NumbersLookupResponse


class TestNumbersLookupResponse(unittest.TestCase):
    """NumbersLookupResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNumbersLookupResponse(self):
        """Test NumbersLookupResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = NumbersLookupResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
