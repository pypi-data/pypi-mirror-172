import sys
import unittest

import smscx_client
from smscx_client.model.data_number_lookup import DataNumberLookup
from smscx_client.model.info_numbers_lookup import InfoNumbersLookup
globals()['DataNumberLookup'] = DataNumberLookup
globals()['InfoNumbersLookup'] = InfoNumbersLookup
from smscx_client.model.numbers_bulk_lookup_result import NumbersBulkLookupResult


class TestNumbersBulkLookupResult(unittest.TestCase):
    """NumbersBulkLookupResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNumbersBulkLookupResult(self):
        """Test NumbersBulkLookupResult"""
        # FIXME: construct object with mandatory attributes with example values
        # model = NumbersBulkLookupResult()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
