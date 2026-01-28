"""
Tests for the models in the aa_permission_management app.
"""

# AA Permission Management
from aa_permission_management.models import General
from aa_permission_management.tests import BaseTestCase


class TestModelGeneral(BaseTestCase):
    """
    Tests for the General model.
    """

    def test_sets_correct_permissions_for_general_model(self):
        """
        Test that the General model has the correct permissions set.

        :return:
        :rtype:
        """

        meta = General._meta

        self.assertIn(
            (
                "access_permission_management",
                "Can access the Permission Management module and manage permissions",
            ),
            meta.permissions,
        )

    def test_does_not_allow_default_permissions_for_general_model(self):
        """
        Test that the General model does not have default permissions.

        :return:
        :rtype:
        """

        meta = General._meta

        self.assertEqual(meta.default_permissions, ())

    def test_does_not_manage_general_model_table(self):
        """
        Test that the General model does not manage its database table.

        :return:
        :rtype:
        """

        meta = General._meta

        self.assertFalse(meta.managed)

    def test_sets_verbose_name_for_general_model(self):
        """
        Test that the General model has the correct verbose name.

        :return:
        :rtype:
        """

        meta = General._meta

        self.assertEqual(meta.verbose_name, "Permission Management")
