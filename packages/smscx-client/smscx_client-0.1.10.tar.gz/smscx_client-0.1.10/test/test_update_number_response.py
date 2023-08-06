import sys
import unittest

import smscx_client
from smscx_client.model.info_phone_number_update import InfoPhoneNumberUpdate
globals()['InfoPhoneNumberUpdate'] = InfoPhoneNumberUpdate
from smscx_client.model.update_number_response import UpdateNumberResponse


class TestUpdateNumberResponse(unittest.TestCase):
    """UpdateNumberResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUpdateNumberResponse(self):
        """Test UpdateNumberResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = UpdateNumberResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
