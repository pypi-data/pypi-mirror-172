import unittest

import smscx_client
from smscx_client.api.numbers_api import NumbersApi  # noqa: E501


class TestNumbersApi(unittest.TestCase):
    """NumbersApi unit test stubs"""

    def setUp(self):
        self.api = NumbersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_cancel_rent(self):
        """Test case for cancel_rent

        Cancel rent for phone number  # noqa: E501
        """
        pass

    def test_get_available_numbers(self):
        """Test case for get_available_numbers

        Get available numbers for rent  # noqa: E501
        """
        pass

    def test_get_bulk_lookup_status(self):
        """Test case for get_bulk_lookup_status

        Get Bulk Lookup result  # noqa: E501
        """
        pass

    def test_get_inbound_sms(self):
        """Test case for get_inbound_sms

        Get inbound SMS from rented number  # noqa: E501
        """
        pass

    def test_get_rent_status(self):
        """Test case for get_rent_status

        Get status of rent  # noqa: E501
        """
        pass

    def test_get_rented_numbers(self):
        """Test case for get_rented_numbers

        Get list of your rented numbers  # noqa: E501
        """
        pass

    def test_get_single_lookup_status(self):
        """Test case for get_single_lookup_status

        Get Single Lookup result  # noqa: E501
        """
        pass

    def test_lookup_number(self):
        """Test case for lookup_number

        Lookup number  # noqa: E501
        """
        pass

    def test_lookup_numbers(self):
        """Test case for lookup_numbers

        Lookup numbers in bulk  # noqa: E501
        """
        pass

    def test_renew_rent(self):
        """Test case for renew_rent

        Renew rent for phone number  # noqa: E501
        """
        pass

    def test_rent_number(self):
        """Test case for rent_number

        Rent phone number  # noqa: E501
        """
        pass

    def test_validate_number(self):
        """Test case for validate_number

        Validate number  # noqa: E501
        """
        pass

    def test_validate_numbers(self):
        """Test case for validate_numbers

        Validate numbers in bulk  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
