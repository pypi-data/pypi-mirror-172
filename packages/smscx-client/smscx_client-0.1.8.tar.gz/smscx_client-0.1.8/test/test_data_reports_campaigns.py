import sys
import unittest

import smscx_client
from smscx_client.model.group import Group
from smscx_client.model.status import Status
globals()['Group'] = Group
globals()['Status'] = Status
from smscx_client.model.data_reports_campaigns import DataReportsCampaigns


class TestDataReportsCampaigns(unittest.TestCase):
    """DataReportsCampaigns unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataReportsCampaigns(self):
        """Test DataReportsCampaigns"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataReportsCampaigns()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
