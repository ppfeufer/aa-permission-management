"""
Unit tests for aa_permission_management.helper.views
"""

# Standard Library
from unittest.mock import MagicMock, patch

# Django
from django.contrib.auth.models import Permission

# Alliance Auth
from allianceauth.authentication.models import State
from allianceauth.groupmanagement.models import AuthGroup

# AA Permission Management
from aa_permission_management.helper.views import (
    get_all_permissions,
    get_group_permissions,
    get_state_permissions,
    set_group_permissions,
    set_state_permissions,
)
from aa_permission_management.tests import BaseTestCase


class TestGetGroupPermissions(BaseTestCase):
    """
    Test cases for get_group_permissions function.
    """

    def test_returns_permissions_for_existing_group(self):
        """
        Test that the function returns the correct permissions for an existing group.

        :return:
        :rtype:
        """

        mock_group = MagicMock()
        mock_group.group.permissions.all.return_value = ["perm1", "perm2"]
        AuthGroup.objects.get = MagicMock(return_value=mock_group)

        result = get_group_permissions(1)

        self.assertEqual(result, ["perm1", "perm2"])

    def test_raises_value_error_for_nonexistent_group(self):
        """
        Test that the function raises a ValueError when the group does not exist.

        :return:
        :rtype:
        """

        AuthGroup.objects.get = MagicMock(side_effect=AuthGroup.DoesNotExist)

        with self.assertRaises(ValueError) as context:
            get_group_permissions(999)

        self.assertEqual(str(context.exception), "Group does not exist")


class TestSetGroupPermissions(BaseTestCase):
    """
    Test cases for set_group_permissions function.
    """

    def test_sets_permissions_for_existing_group(self):
        """
        Test that the function sets the correct permissions for an existing group.

        :return:
        :rtype:
        """

        mock_group = MagicMock()
        AuthGroup.objects.get = MagicMock(return_value=mock_group)

        set_group_permissions(1, ["perm1", "perm2"])

        mock_group.group.permissions.set.assert_called_once_with(["perm1", "perm2"])
        mock_group.group.save.assert_called_once()

    def test_raises_value_error_for_nonexistent_group(self):
        """
        Test that the function raises a ValueError when the group does not exist.

        :return:
        :rtype:
        """

        AuthGroup.objects.get = MagicMock(side_effect=AuthGroup.DoesNotExist)

        with self.assertRaises(ValueError) as context:
            set_group_permissions(999, ["perm1", "perm2"])

        self.assertEqual(str(context.exception), "Group does not exist")


class TestGetStatePermissions(BaseTestCase):
    """
    Test cases for get_state_permissions function.
    """

    def test_returns_permissions_for_existing_state(self):
        """
        Test that the function returns the correct permissions for an existing state.

        :return:
        :rtype:
        """

        mock_state = MagicMock()
        mock_state.permissions.all.return_value = ["perm1", "perm2"]

        with patch(
            "allianceauth.authentication.models.State.objects.get",
            return_value=mock_state,
        ):
            result = get_state_permissions(2)

        self.assertEqual(result, ["perm1", "perm2"])

    def test_raises_value_error_for_nonexistent_state(self):
        """
        Test that the function raises a ValueError when the state does not exist.

        :return:
        :rtype:
        """

        with patch(
            "allianceauth.authentication.models.State.objects.get",
            side_effect=State.DoesNotExist,
        ):
            with self.assertRaises(ValueError) as context:
                get_state_permissions(999)

        self.assertEqual(str(context.exception), "State does not exist")


class TestSetStatePermissions(BaseTestCase):
    """
    Test cases for set_state_permissions function.
    """

    def test_sets_permissions_for_existing_state(self):
        """
        Test that the function sets the correct permissions for an existing state.

        :return:
        :rtype:
        """

        state = State.objects.get(name="Guest")
        permissions = Permission.objects.all()[:2]

        set_state_permissions(state_id=state.pk, permissions=set(permissions))

        self.assertEqual(set(state.permissions.all()), set(permissions))

    def test_raises_error_for_nonexistent_state(self):
        """
        Test that the function raises a ValueError when the state does not exist.

        :return:
        :rtype:
        """

        non_existent_state_id = 999
        permissions = Permission.objects.all()[:2]

        with self.assertRaises(ValueError) as context:
            set_state_permissions(
                state_id=non_existent_state_id, permissions=set(permissions)
            )

        self.assertEqual(str(context.exception), "State does not exist")

    def test_clears_permissions_when_empty_set_provided(self):
        """
        Test that the function clears permissions when an empty set is provided.

        :return:
        :rtype:
        """

        state = State.objects.get(name="Guest")
        permissions = Permission.objects.all()[:2]
        state.permissions.set(permissions)

        set_state_permissions(state_id=state.pk, permissions=set())

        self.assertEqual(set(state.permissions.all()), set())


class TestGetAllPermissions(BaseTestCase):
    """
    Test cases for get_all_permissions function.
    """

    def test_returns_all_permissions(self):
        """
        Test that the function returns all permissions.

        :return:
        :rtype:
        """

        mock_permissions = ["perm1", "perm2", "perm3"]

        with patch(
            "django.contrib.auth.models.Permission.objects.all",
            return_value=mock_permissions,
        ):
            result = get_all_permissions()

        self.assertEqual(result, mock_permissions)

    def test_returns_empty_list_when_no_permissions(self):
        """
        Test that the function returns an empty list when there are no permissions.

        :return:
        :rtype:
        """

        with patch(
            "django.contrib.auth.models.Permission.objects.all", return_value=[]
        ):
            result = get_all_permissions()

        self.assertEqual(result, [])
