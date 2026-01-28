"""
Tests for the auth hooks.
"""

# Django
from django.test import RequestFactory

# AA Permission Management
from aa_permission_management.auth_hooks import PermissionManagementMenuItem
from aa_permission_management.tests import BaseTestCase


class TestPermissionManagementMenuItem(BaseTestCase):
    """
    Tests for the PermissionManagementMenuItem auth hook.
    """

    def test_renders_menu_item_for_authorized_user(self):
        """
        Test that the menu item is rendered for a user with the required permissions.

        :return:
        :rtype:
        """

        request = RequestFactory().get("/")
        request.user = self.user_with_permission

        menu_item = PermissionManagementMenuItem()
        result = menu_item.render(request)

        self.assertIn("fa-solid fa-list-check", result)
        self.assertIn("Permission Management", result)

    def test_does_not_render_menu_item_for_unauthorized_user(self):
        """
        Test that the menu item is not rendered for a user without the required permissions.

        :return:
        :rtype:
        """

        request = RequestFactory().get("/")
        request.user = self.user_without_permission

        menu_item = PermissionManagementMenuItem()
        result = menu_item.render(request)

        self.assertEqual(result, "")
