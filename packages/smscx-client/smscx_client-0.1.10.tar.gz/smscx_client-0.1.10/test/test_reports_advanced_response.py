import sys
import unittest

import smscx_client
from smscx_client.model.data_reports import DataReports
from smscx_client.model.info_reports import InfoReports
from smscx_client.model.paging import Paging
globals()['DataReports'] = DataReports
globals()['InfoReports'] = InfoReports
globals()['Paging'] = Paging
from smscx_client.model.reports_advanced_response import ReportsAdvancedResponse


class TestReportsAdvancedResponse(unittest.TestCase):
    """ReportsAdvancedResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReportsAdvancedResponse(self):
        """Test ReportsAdvancedResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ReportsAdvancedResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
