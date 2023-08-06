import sys
import unittest

import smscx_client
from smscx_client.model.accepted import Accepted
from smscx_client.model.data_summary_delivery import DataSummaryDelivery
from smscx_client.model.delivered import Delivered
from smscx_client.model.failed import Failed
from smscx_client.model.no_coverage import NoCoverage
from smscx_client.model.scheduled import Scheduled
globals()['Accepted'] = Accepted
globals()['DataSummaryDelivery'] = DataSummaryDelivery
globals()['Delivered'] = Delivered
globals()['Failed'] = Failed
globals()['NoCoverage'] = NoCoverage
globals()['Scheduled'] = Scheduled
from smscx_client.model.reports_summary_delivery_response_data_value import ReportsSummaryDeliveryResponseDataValue


class TestReportsSummaryDeliveryResponseDataValue(unittest.TestCase):
    """ReportsSummaryDeliveryResponseDataValue unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReportsSummaryDeliveryResponseDataValue(self):
        """Test ReportsSummaryDeliveryResponseDataValue"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ReportsSummaryDeliveryResponseDataValue()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
