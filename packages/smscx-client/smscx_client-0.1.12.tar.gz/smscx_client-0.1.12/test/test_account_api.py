import unittest

import smscx_client
from smscx_client.api.account_api import AccountApi  # noqa: E501


class TestAccountApi(unittest.TestCase):
    """AccountApi unit test stubs"""

    def setUp(self):
        self.api = AccountApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_account_balance(self):
        """Test case for get_account_balance

        Get account balance  # noqa: E501
        """
        pass

    def test_get_channel_pricing(self):
        """Test case for get_channel_pricing

        Get channels pricing  # noqa: E501
        """
        pass

    def test_get_channel_pricing_by_country_iso(self):
        """Test case for get_channel_pricing_by_country_iso

        Get pricing for channel by country iso  # noqa: E501
        """
        pass

    def test_get_channels_status(self):
        """Test case for get_channels_status

        Get status of all channels  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
