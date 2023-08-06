import sys
import unittest

import smscx_client
from smscx_client.model.rich_media import RichMedia
globals()['RichMedia'] = RichMedia
from smscx_client.model.data_template import DataTemplate


class TestDataTemplate(unittest.TestCase):
    """DataTemplate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDataTemplate(self):
        """Test DataTemplate"""
        # FIXME: construct object with mandatory attributes with example values
        # model = DataTemplate()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
