import unittest

import smscx_client
from smscx_client.api.viber_api import ViberApi  # noqa: E501


class TestViberApi(unittest.TestCase):
    """ViberApi unit test stubs"""

    def setUp(self):
        self.api = ViberApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_scheduled_viber_campaign(self):
        """Test case for delete_scheduled_viber_campaign

        Delete scheduled Viber campaign  # noqa: E501
        """
        pass

    def test_delete_scheduled_viber_message(self):
        """Test case for delete_scheduled_viber_message

        Delete scheduled Viber message  # noqa: E501
        """
        pass

    def test_estimate_viber_campaign(self):
        """Test case for estimate_viber_campaign

        Estimate Viber campaign  # noqa: E501
        """
        pass

    def test_estimate_viber_message(self):
        """Test case for estimate_viber_message

        Estimate Viber message  # noqa: E501
        """
        pass

    def test_send_viber_campaign(self):
        """Test case for send_viber_campaign

        Send Viber campaign  # noqa: E501
        """
        pass

    def test_send_viber_message(self):
        """Test case for send_viber_message

        Send Viber message  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
