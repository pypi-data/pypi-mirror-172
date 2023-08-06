import sys
import unittest

import smscx_client
from smscx_client.model.data_reports_campaigns import DataReportsCampaigns
from smscx_client.model.info_reports_campaigns import InfoReportsCampaigns
from smscx_client.model.paging import Paging
globals()['DataReportsCampaigns'] = DataReportsCampaigns
globals()['InfoReportsCampaigns'] = InfoReportsCampaigns
globals()['Paging'] = Paging
from smscx_client.model.reports_campaigns_respone import ReportsCampaignsRespone


class TestReportsCampaignsRespone(unittest.TestCase):
    """ReportsCampaignsRespone unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReportsCampaignsRespone(self):
        """Test ReportsCampaignsRespone"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ReportsCampaignsRespone()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
