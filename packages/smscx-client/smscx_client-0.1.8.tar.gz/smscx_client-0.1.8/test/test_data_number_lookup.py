import sys
import unittest

import smscx_client
from smscx_client.model.original_network import OriginalNetwork
from smscx_client.model.ported_network import PortedNetwork
from smscx_client.model.roaming_network import RoamingNetwork
globals()['OriginalNetwork'] = OriginalNetwork
globals()['PortedNetwork'] = PortedNetwork
globals()['RoamingNetwork'] = RoamingNetwork
from smscx_client.model.data_number_lookup import DataNumberLookup


class TestDataNumberLookup(unittest.TestCase):
    """DataNumberLookup unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataNumberLookup(self):
        """Test DataNumberLookup"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataNumberLookup()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
