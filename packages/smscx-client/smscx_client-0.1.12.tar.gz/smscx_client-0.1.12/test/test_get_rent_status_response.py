import sys
import unittest

import smscx_client
from smscx_client.model.info_rent_number import InfoRentNumber
globals()['InfoRentNumber'] = InfoRentNumber
from smscx_client.model.get_rent_status_response import GetRentStatusResponse


class TestGetRentStatusResponse(unittest.TestCase):
    """GetRentStatusResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetRentStatusResponse(self):
        """Test GetRentStatusResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GetRentStatusResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
