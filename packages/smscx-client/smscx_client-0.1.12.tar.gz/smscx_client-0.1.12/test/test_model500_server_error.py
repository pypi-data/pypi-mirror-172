import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
globals()['Error'] = Error
from smscx_client.model.model500_server_error import Model500ServerError


class TestModel500ServerError(unittest.TestCase):
    """Model500ServerError unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel500ServerError(self):
        """Test Model500ServerError"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Model500ServerError()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
