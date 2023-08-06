import sys
import unittest

import smscx_client
from smscx_client.model.data_optouts import DataOptouts
from smscx_client.model.info_optouts import InfoOptouts
from smscx_client.model.paging import Paging
globals()['DataOptouts'] = DataOptouts
globals()['InfoOptouts'] = InfoOptouts
globals()['Paging'] = Paging
from smscx_client.model.optouts_list_response import OptoutsListResponse


class TestOptoutsListResponse(unittest.TestCase):
    """OptoutsListResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOptoutsListResponse(self):
        """Test OptoutsListResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = OptoutsListResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
