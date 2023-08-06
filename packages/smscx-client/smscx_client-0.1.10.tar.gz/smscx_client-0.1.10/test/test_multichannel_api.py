import unittest

import smscx_client
from smscx_client.api.multichannel_api import MultichannelApi  # noqa: E501


class TestMultichannelApi(unittest.TestCase):
    """MultichannelApi unit test stubs"""

    def setUp(self):
        self.api = MultichannelApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_scheduled_multichannel_campaign(self):
        """Test case for delete_scheduled_multichannel_campaign

        Delete scheduled Multichannel campaign  # noqa: E501
        """
        pass

    def test_delete_scheduled_multichannel_message(self):
        """Test case for delete_scheduled_multichannel_message

        Delete scheduled Multichannel message  # noqa: E501
        """
        pass

    def test_estimate_multichannel_campaign(self):
        """Test case for estimate_multichannel_campaign

        Estimate Multichannel campaign  # noqa: E501
        """
        pass

    def test_estimate_multichannel_message(self):
        """Test case for estimate_multichannel_message

        Estimate Multichannel message  # noqa: E501
        """
        pass

    def test_send_multichannel_campaign(self):
        """Test case for send_multichannel_campaign

        Send Multichannel campaign  # noqa: E501
        """
        pass

    def test_send_multichannel_message(self):
        """Test case for send_multichannel_message

        Send Multichannel message  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
