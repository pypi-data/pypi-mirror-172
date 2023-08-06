import sys
import unittest

import smscx_client
from smscx_client.model.rental_cost import RentalCost
globals()['RentalCost'] = RentalCost
from smscx_client.model.data_rented_numbers import DataRentedNumbers


class TestDataRentedNumbers(unittest.TestCase):
    """DataRentedNumbers unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataRentedNumbers(self):
        """Test DataRentedNumbers"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataRentedNumbers()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
