"""
Tests for the views in the aa_permission_management app.
"""

# Standard Library
import json
from http import HTTPStatus
from unittest.mock import MagicMock, patch

# Django
from django.test import RequestFactory
from django.urls import reverse

# Alliance Auth
from allianceauth.groupmanagement.models import AuthGroup

# AA Permission Management
from aa_permission_management.tests import BaseTestCase
from aa_permission_management.views import (
    GroupsTableView,
    StatesTableView,
    ajax_update_permissions,
)


class TestViewDashboard(BaseTestCase):
    """
    Tests for the dashboard view.
    """

    def test_allows_access_to_authorized_user(self):
        """
        Test that an authorized user can access the dashboard view.

        :return:
        :rtype:
        """

        self.client.force_login(self.user_with_permission)

        response = self.client.get(reverse("aa_permission_management:dashboard"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(b"Permission Management", response.content)
        self.assertTemplateUsed(
            response, "aa_permission_management/views/dashboard.html"
        )

    def test_denies_access_to_unauthorized_user(self):
        """
        Test that an unauthorized user is denied access to the dashboard view.

        :return:
        :rtype:
        """

        self.client.force_login(self.user_without_permission)

        response = self.client.get(reverse("aa_permission_management:dashboard"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class TestGroupsTableView(BaseTestCase):
    """
    Tests for the GroupsTableView view.
    """

    def test_returns_queryset_with_related_group(self):
        """
        Test that the get_model_qs method returns a queryset with related group.

        :return:
        :rtype:
        """

        factory = RequestFactory()
        request = factory.get(reverse("aa_permission_management:get_groups"))
        request.user = self.user_with_permission

        view = GroupsTableView()
        queryset = view.get_model_qs(request)

        self.assertTrue(queryset.query.select_related)
        self.assertIn("group", queryset.query.select_related)

    def test_handles_empty_queryset_correctly(self):
        """
        Test that the get_model_qs method handles an empty queryset correctly.

        :return:
        :rtype:
        """

        factory = RequestFactory()
        request = factory.get(reverse("aa_permission_management:get_groups"))
        request.user = self.user_with_permission

        AuthGroup.objects.all().delete()

        view = GroupsTableView()
        queryset = view.get_model_qs(request)

        self.assertEqual(queryset.count(), 0)


class TestStatesTableView(BaseTestCase):
    """
    Tests for the StatesTableView view.
    """

    def test_returns_queryset_with_user_count_annotation(self):
        """
        Test that the get_model_qs method returns a queryset with user_count annotation.

        :return:
        :rtype:
        """

        factory = RequestFactory()
        request = factory.get(reverse("aa_permission_management:get_states"))
        request.user = self.user_with_permission

        view = StatesTableView()
        queryset = view.get_model_qs(request)

        self.assertTrue(queryset.exists())
        self.assertIn("user_count", queryset.query.annotations)


class TestAjaxGetPermissionsView(BaseTestCase):
    """
    Tests for the ajax_get_permissions view.
    """

    def test_returns_permissions_for_group(self):
        """
        Test that the view returns the correct permissions for a group.

        :return:
        :rtype:
        """

        mock_permissions = ["perm1", "perm2"]
        all_permissions = ["perm1", "perm2", "perm3"]

        self.client.force_login(self.user_with_permission)

        with (
            patch(
                "aa_permission_management.views.get_group_permissions",
                return_value=mock_permissions,
            ),
            patch(
                "aa_permission_management.views.get_all_permissions",
                return_value=all_permissions,
            ),
        ):
            response = self.client.get(
                reverse(
                    "aa_permission_management:get_permissions",
                    kwargs={"permission_type": "group", "element_id": 1},
                )
            )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("assigned_permissions", response.context)
        self.assertEqual(response.context["assigned_permissions"], mock_permissions)

        expected_available = [p for p in all_permissions if p not in mock_permissions]
        self.assertEqual(response.context["permissions"], expected_available)

    def test_returns_permissions_for_state(self):
        """
        Test that the view returns the correct permissions for a state.

        :return:
        :rtype:
        """

        mock_permissions = ["perm1", "perm2"]
        all_permissions = ["perm1", "perm2", "perm3"]

        self.client.force_login(self.user_with_permission)

        with (
            patch(
                "aa_permission_management.views.get_state_permissions",
                return_value=mock_permissions,
            ),
            patch(
                "aa_permission_management.views.get_all_permissions",
                return_value=all_permissions,
            ),
        ):
            response = self.client.get(
                reverse(
                    "aa_permission_management:get_permissions",
                    kwargs={"permission_type": "state", "element_id": 2},
                )
            )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("assigned_permissions", response.context)
        self.assertEqual(response.context["assigned_permissions"], mock_permissions)

        expected_available = [p for p in all_permissions if p not in mock_permissions]
        self.assertEqual(response.context["permissions"], expected_available)

    def test_raises_value_error_for_invalid_type(self):
        """
        Test that the view raises a ValueError for an invalid type.

        :return:
        :rtype:
        """

        self.client.force_login(self.user_with_permission)

        with self.assertRaises(ValueError):
            self.client.get(
                reverse(
                    "aa_permission_management:get_permissions",
                    kwargs={"permission_type": "invalid", "element_id": 3},
                )
            )


class TestAjaxUpdatePermissionsView(BaseTestCase):
    """
    Tests for the ajax_update_permissions view.
    """

    def test_returns_success_when_updating_group_permissions(self):
        """
        Test that the view returns a success response when updating group permissions.

        :return:
        :rtype:
        """

        request = MagicMock()
        request.method = "POST"
        request.body = json.dumps(
            {
                "permission_type": "group",
                "element_id": 1,
                "permissions": ["perm1", "perm2"],
            }
        )

        with patch(
            "aa_permission_management.views.set_group_permissions"
        ) as mock_set_permissions:
            response = ajax_update_permissions(request)

        mock_set_permissions.assert_called_once_with(1, {"perm1", "perm2"})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode(), "Success")

    def test_returns_success_when_updating_state_permissions(self):
        """
        Test that the view returns a success response when updating state permissions.

        :return:
        :rtype:
        """

        request = MagicMock()
        request.method = "POST"
        request.body = json.dumps(
            {"permission_type": "state", "element_id": 2, "permissions": ["perm3"]}
        )

        with patch(
            "aa_permission_management.views.set_state_permissions"
        ) as mock_set_permissions:
            response = ajax_update_permissions(request)

        mock_set_permissions.assert_called_once_with(2, {"perm3"})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode(), "Success")

    def test_returns_no_content_when_request_method_is_not_post(self):
        """
        Test that the view returns a no content response when the request method is not POST.

        :return:
        :rtype:
        """

        request = MagicMock()
        request.method = "GET"

        response = ajax_update_permissions(request)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_returns_no_content_when_request_body_is_invalid_json(self):
        """
        Test that the view returns a no content response when the request body is invalid JSON.

        :return:
        :rtype:
        """

        request = MagicMock()
        request.method = "POST"
        request.body = "invalid json"

        response = ajax_update_permissions(request)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_returns_no_content_when_required_keys_are_missing(self):
        """
        Test that the view returns a no content response when required keys are missing from the request body.

        :return:
        :rtype:
        """

        request = MagicMock()
        request.method = "POST"
        request.body = json.dumps({"permission_type": "group", "element_id": 1})

        response = ajax_update_permissions(request)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_returns_no_content_and_error_message_when_permission_type_is_invalid(self):
        """
        Test that the view returns a no content response and an error message when the permission type is invalid.

        :return:
        :rtype:
        """

        request = MagicMock()
        request.method = "POST"
        request.body = json.dumps(
            {"permission_type": "invalid", "element_id": 1, "permissions": ["perm1"]}
        )

        response = ajax_update_permissions(request)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(response.content.decode(), "Error: Invalid Permission Type")
