import sys
import unittest

import smscx_client
from smscx_client.model.data_number_lookup_webhook import DataNumberLookupWebhook
globals()['DataNumberLookupWebhook'] = DataNumberLookupWebhook
from smscx_client.model.call_back_request_number_lookup import CallBackRequestNumberLookup


class TestCallBackRequestNumberLookup(unittest.TestCase):
    """CallBackRequestNumberLookup unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCallBackRequestNumberLookup(self):
        """Test CallBackRequestNumberLookup"""
        # FIXME: construct object with mandatory attributes with example values
        # model = CallBackRequestNumberLookup()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
