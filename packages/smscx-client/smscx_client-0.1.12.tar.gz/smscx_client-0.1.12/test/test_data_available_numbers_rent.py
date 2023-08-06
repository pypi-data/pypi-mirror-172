import sys
import unittest

import smscx_client
from smscx_client.model.rental_cost import RentalCost
globals()['RentalCost'] = RentalCost
from smscx_client.model.data_available_numbers_rent import DataAvailableNumbersRent


class TestDataAvailableNumbersRent(unittest.TestCase):
    """DataAvailableNumbersRent unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataAvailableNumbersRent(self):
        """Test DataAvailableNumbersRent"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataAvailableNumbersRent()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
