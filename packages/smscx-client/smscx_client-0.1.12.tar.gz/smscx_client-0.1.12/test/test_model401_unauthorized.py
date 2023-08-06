import sys
import unittest

import smscx_client
from smscx_client.model.error import Error
globals()['Error'] = Error
from smscx_client.model.model401_unauthorized import Model401Unauthorized


class TestModel401Unauthorized(unittest.TestCase):
    """Model401Unauthorized unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testModel401Unauthorized(self):
        """Test Model401Unauthorized"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Model401Unauthorized()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
