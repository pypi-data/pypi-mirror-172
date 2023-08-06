import sys
import unittest

import smscx_client
from smscx_client.model.country_price_obj1 import CountryPriceObj1
globals()['CountryPriceObj1'] = CountryPriceObj1
from smscx_client.model.country_price_obj import CountryPriceObj


class TestCountryPriceObj(unittest.TestCase):
    """CountryPriceObj unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCountryPriceObj(self):
        """Test CountryPriceObj"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CountryPriceObj()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
