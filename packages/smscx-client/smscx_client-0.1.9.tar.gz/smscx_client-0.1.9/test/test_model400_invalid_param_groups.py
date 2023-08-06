import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
globals()['Error'] = Error
from smscx_client.model.model400_invalid_param_groups import Model400InvalidParamGroups


class TestModel400InvalidParamGroups(unittest.TestCase):
    """Model400InvalidParamGroups unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel400InvalidParamGroups(self):
        """Test Model400InvalidParamGroups"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Model400InvalidParamGroups()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
