import unittest

import smscx_client
from smscx_client.api.attachments_api import AttachmentsApi  # noqa: E501


class TestAttachmentsApi(unittest.TestCase):
    """AttachmentsApi unit test stubs"""

    def setUp(self):
        self.api = AttachmentsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_attachment(self):
        """Test case for delete_attachment

        Delete attachment  # noqa: E501
        """
        pass

    def test_export_attachment_hits_to_csv(self):
        """Test case for export_attachment_hits_to_csv

        Export attachment hits to CSV  # noqa: E501
        """
        pass

    def test_export_attachment_hits_to_xlsx(self):
        """Test case for export_attachment_hits_to_xlsx

        Export attachment hits to XLSX  # noqa: E501
        """
        pass

    def test_get_attachment_hits(self):
        """Test case for get_attachment_hits

        Get attachment hits  # noqa: E501
        """
        pass

    def test_get_attachments_list(self):
        """Test case for get_attachments_list

        Get attachments list  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
