import sys
import unittest

import smscx_client
from smscx_client.model.reports_summary_channel_response import ReportsSummaryChannelResponse
from smscx_client.model.reports_summary_country_response import ReportsSummaryCountryResponse
from smscx_client.model.reports_summary_delivery_response import ReportsSummaryDeliveryResponse
from smscx_client.model.reports_summary_source_response import ReportsSummarySourceResponse
from smscx_client.model.reports_summary_traffic_response import ReportsSummaryTrafficResponse
from smscx_client.model.reports_summary_traffic_response_data_value import ReportsSummaryTrafficResponseDataValue
globals()['ReportsSummaryChannelResponse'] = ReportsSummaryChannelResponse
globals()['ReportsSummaryCountryResponse'] = ReportsSummaryCountryResponse
globals()['ReportsSummaryDeliveryResponse'] = ReportsSummaryDeliveryResponse
globals()['ReportsSummarySourceResponse'] = ReportsSummarySourceResponse
globals()['ReportsSummaryTrafficResponse'] = ReportsSummaryTrafficResponse
globals()['ReportsSummaryTrafficResponseDataValue'] = ReportsSummaryTrafficResponseDataValue
from smscx_client.model.get_summary_reports200_response import GetSummaryReports200Response


class TestGetSummaryReports200Response(unittest.TestCase):
    """GetSummaryReports200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetSummaryReports200Response(self):
        """Test GetSummaryReports200Response"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GetSummaryReports200Response()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
