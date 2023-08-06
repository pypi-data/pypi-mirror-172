import unittest

import smscx_client
from smscx_client.api.oauth_api import OauthApi  # noqa: E501


class TestOauthApi(unittest.TestCase):
    """OauthApi unit test stubs"""

    def setUp(self):
        self.api = OauthApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_access_token(self):
        """Test case for get_access_token

        Get access token  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
