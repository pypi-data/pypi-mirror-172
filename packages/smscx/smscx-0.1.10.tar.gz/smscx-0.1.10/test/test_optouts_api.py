import unittest

import smscx_client
from smscx_client.api.optouts_api import OptoutsApi  # noqa: E501


class TestOptoutsApi(unittest.TestCase):
    """OptoutsApi unit test stubs"""

    def setUp(self):
        self.api = OptoutsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_contact_to_optouts_list(self):
        """Test case for add_contact_to_optouts_list

        Add contact to optouts list  # noqa: E501
        """
        pass

    def test_delete_contact_from_optouts_list(self):
        """Test case for delete_contact_from_optouts_list

        Delete contact from optouts list  # noqa: E501
        """
        pass

    def test_export_optouts_to_csv(self):
        """Test case for export_optouts_to_csv

        Export optouts to CSV  # noqa: E501
        """
        pass

    def test_export_optouts_to_xlsx(self):
        """Test case for export_optouts_to_xlsx

        Export optouts to XLSX  # noqa: E501
        """
        pass

    def test_get_optouts_list(self):
        """Test case for get_optouts_list

        Get optouts list  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
