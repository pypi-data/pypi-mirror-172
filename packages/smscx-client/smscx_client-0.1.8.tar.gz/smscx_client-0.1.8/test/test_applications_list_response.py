import sys
import unittest

import smscx_client
from smscx_client.model.data_applications_list import DataApplicationsList
globals()['DataApplicationsList'] = DataApplicationsList
from smscx_client.model.applications_list_response import ApplicationsListResponse


class TestApplicationsListResponse(unittest.TestCase):
    """ApplicationsListResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testApplicationsListResponse(self):
        """Test ApplicationsListResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ApplicationsListResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
