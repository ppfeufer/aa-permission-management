"""
Helper functions for the views in aa_permission_management.
"""

# Standard Library
from collections.abc import Iterable
from typing import Any

# Alliance Auth
from allianceauth.authentication.models import Permission, State
from allianceauth.groupmanagement.models import AuthGroup


def _get_permissions_to_set(permissions: Iterable[str]) -> list[str] | list[str | Any]:
    """
    Get permissions IDs iterable from permissions iterable.

    :param permissions:
    :type permissions:
    :return:
    :rtype:
    """

    # Convert permission model instances to primary key values so `.set()`
    # works whether the caller provides Permission instances or IDs.
    if isinstance(permissions, (str, bytes)):
        # treat a single string/bytes as a single permission value
        perms_to_set = [permissions]
    else:
        perms_to_set = [getattr(p, "pk", p) for p in permissions]

    return perms_to_set


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


def set_group_permissions(group_id: int, permissions: Iterable[str]) -> None:
    """
    Set permissions for a specific group.

    :param group_id: ID of the group
    :type group_id: int
    :param permissions: List of permissions to set
    :type permissions: list
    """

    try:
        group = AuthGroup.objects.get(pk=group_id)
        group.group.permissions.set(_get_permissions_to_set(permissions))
        group.group.save()
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


def set_state_permissions(state_id: int, permissions: Iterable[str]) -> None:
    """
    Set permissions for a specific state.

    :param state_id: ID of the state
    :type state_id: int
    :param permissions: List of permissions to set
    :type permissions: list
    """

    try:
        state = State.objects.get(pk=state_id)
        state.permissions.set(_get_permissions_to_set(permissions))
        state.save()
    except State.DoesNotExist as exc:
        raise ValueError("State does not exist") from exc


def get_all_permissions() -> list:
    """
    Get all Django permissions.

    :return: List of all unique permissions
    :rtype: list
    """

    return list(Permission.objects.all())
