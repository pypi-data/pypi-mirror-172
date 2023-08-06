import unittest

import smscx_client
from smscx_client.api.reports_api import ReportsApi  # noqa: E501


class TestReportsApi(unittest.TestCase):
    """ReportsApi unit test stubs"""

    def setUp(self):
        self.api = ReportsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_export_advanced_report_to_csv(self):
        """Test case for export_advanced_report_to_csv

        Export advanced report to CSV  # noqa: E501
        """
        pass

    def test_export_advanced_report_to_xlsx(self):
        """Test case for export_advanced_report_to_xlsx

        Export advanced report to XLSX  # noqa: E501
        """
        pass

    def test_export_campaign_report_to_csv(self):
        """Test case for export_campaign_report_to_csv

        Export campaign report to CSV  # noqa: E501
        """
        pass

    def test_export_campaign_report_to_xlsx(self):
        """Test case for export_campaign_report_to_xlsx

        Export campaign report to XLSX  # noqa: E501
        """
        pass

    def test_get_advanced_report(self):
        """Test case for get_advanced_report

        Get advanced report  # noqa: E501
        """
        pass

    def test_get_campaign_report(self):
        """Test case for get_campaign_report

        Get campaign report  # noqa: E501
        """
        pass

    def test_get_campaigns_list(self):
        """Test case for get_campaigns_list

        Get list of sent campaigns  # noqa: E501
        """
        pass

    def test_get_single_report(self):
        """Test case for get_single_report

        Get report for single SMS or Viber or Whatsapp or Multichannel  # noqa: E501
        """
        pass

    def test_get_summary_reports(self):
        """Test case for get_summary_reports

        Get summary reports for a dimension  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
