"""
Helper functions for the views in aa_permission_management.
"""

# Django
from django.contrib.auth.models import Permission

# Alliance Auth
from allianceauth.authentication.models import State
from allianceauth.groupmanagement.models import AuthGroup


def get_group_permissions(group_id: int) -> list:
    """
    Get permissions for a specific group.

    :param group_id: ID of the group
    :type group_id: int
    :return: List of permissions
    :rtype: list
    """

    try:
        group = AuthGroup.objects.get(pk=group_id)

        return list(group.group.permissions.all())
    except AuthGroup.DoesNotExist as exc:
        raise ValueError("Group does not exist") from exc


def get_state_permissions(state_id: int) -> list:
    """
    Get permissions for a specific state.

    :param state_id: ID of the state
    :type state_id: int
    :return: List of permissions
    :rtype: list
    """

    try:
        state = State.objects.get(pk=state_id)

        return list(state.permissions.all())
    except State.DoesNotExist as exc:
        raise ValueError("State does not exist") from exc


def get_all_permissions() -> list:
    """
    Get all Django permissions.

    :return: List of all unique permissions
    :rtype: list
    """

    return list(Permission.objects.all())
