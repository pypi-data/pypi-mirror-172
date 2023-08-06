import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
globals()['Error'] = Error
from smscx_client.model.model400_invalid_param import Model400InvalidParam


class TestModel400InvalidParam(unittest.TestCase):
    """Model400InvalidParam unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel400InvalidParam(self):
        """Test Model400InvalidParam"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Model400InvalidParam()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
