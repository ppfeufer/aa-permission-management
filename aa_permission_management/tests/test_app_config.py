"""
Tests for the PermissionManagementConfig app configuration.
"""

# Standard Library
import importlib

# Django
from django.utils.text import format_lazy

# AA Permission Management
from aa_permission_management import __title_translated__, __version__
from aa_permission_management.apps import PermissionManagementConfig
from aa_permission_management.tests import BaseTestCase


class TestAppConfig(BaseTestCase):
    """
    Tests for the PermissionManagementConfig app configuration.
    """

    def test_initializes_with_correct_name(self):
        """
        Test that the PermissionManagementConfig initializes with the correct name.

        :return:
        :rtype:
        """

        config = PermissionManagementConfig(
            "aa_permission_management",
            importlib.import_module("aa_permission_management"),
        )

        self.assertEqual(config.name, "aa_permission_management")

    def test_initializes_with_correct_label(self):
        """
        Test that the PermissionManagementConfig initializes with the correct label.

        :return:
        :rtype:
        """

        config = PermissionManagementConfig(
            "aa_permission_management",
            importlib.import_module("aa_permission_management"),
        )

        self.assertEqual(config.label, "aa_permission_management")

    def test_initializes_with_correct_verbose_name(self):
        """
        Test that the PermissionManagementConfig initializes with the correct verbose name.

        :return:
        :rtype:
        """

        config = PermissionManagementConfig(
            "aa_permission_management",
            importlib.import_module("aa_permission_management"),
        )

        expected = format_lazy(
            "{app_title} v{version}",
            app_title=__title_translated__,
            version=__version__,
        )

        self.assertEqual(config.verbose_name, expected)
