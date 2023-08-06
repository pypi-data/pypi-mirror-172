import unittest

import smscx_client
from smscx_client.api.applications_api import ApplicationsApi  # noqa: E501


class TestApplicationsApi(unittest.TestCase):
    """ApplicationsApi unit test stubs"""

    def setUp(self):
        self.api = ApplicationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_application_settings(self):
        """Test case for get_application_settings

        Get application settings  # noqa: E501
        """
        pass

    def test_get_applications_list(self):
        """Test case for get_applications_list

        Get applications list  # noqa: E501
        """
        pass

    def test_get_scopes(self):
        """Test case for get_scopes

        Get scopes  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
