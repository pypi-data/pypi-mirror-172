import sys
import unittest

import smscx_client
from smscx_client.model.data_rented_numbers import DataRentedNumbers
globals()['DataRentedNumbers'] = DataRentedNumbers
from smscx_client.model.rented_numbers_response import RentedNumbersResponse


class TestRentedNumbersResponse(unittest.TestCase):
    """RentedNumbersResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRentedNumbersResponse(self):
        """Test RentedNumbersResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = RentedNumbersResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
