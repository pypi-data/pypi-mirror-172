import sys
import unittest

import smscx_client
from smscx_client.model.data_originators_list import DataOriginatorsList
globals()['DataOriginatorsList'] = DataOriginatorsList
from smscx_client.model.originators_list_response import OriginatorsListResponse


class TestOriginatorsListResponse(unittest.TestCase):
    """OriginatorsListResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOriginatorsListResponse(self):
        """Test OriginatorsListResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = OriginatorsListResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
