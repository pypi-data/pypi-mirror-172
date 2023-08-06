import sys
import unittest

import smscx_client
from smscx_client.model.info_optout import InfoOptout
globals()['InfoOptout'] = InfoOptout
from smscx_client.model.optouts_delete_response import OptoutsDeleteResponse


class TestOptoutsDeleteResponse(unittest.TestCase):
    """OptoutsDeleteResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOptoutsDeleteResponse(self):
        """Test OptoutsDeleteResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = OptoutsDeleteResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
