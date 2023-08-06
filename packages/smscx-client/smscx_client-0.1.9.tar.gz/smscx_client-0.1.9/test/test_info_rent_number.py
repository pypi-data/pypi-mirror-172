import sys
import unittest

import smscx_client
from smscx_client.model.rental_cost import RentalCost
globals()['RentalCost'] = RentalCost
from smscx_client.model.info_rent_number import InfoRentNumber


class TestInfoRentNumber(unittest.TestCase):
    """InfoRentNumber unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInfoRentNumber(self):
        """Test InfoRentNumber"""
        # FIXME: construct object with mandatory attributes with example values
        # model = InfoRentNumber()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
