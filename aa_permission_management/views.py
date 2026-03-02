"""
Views for the AA Permission Management app.
"""

# Standard Library
import json
from http import HTTPStatus

# Django
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Alliance Auth
from allianceauth.authentication.models import State
from allianceauth.framework.datatables import DataTablesView
from allianceauth.groupmanagement.models import AuthGroup
from allianceauth.services.hooks import get_extension_logger

# AA Permission Management
from aa_permission_management import __title__
from aa_permission_management.helper.views import (
    get_all_permissions,
    get_group_permissions,
    get_state_permissions,
    set_group_permissions,
    set_state_permissions,
)
from aa_permission_management.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


@permission_required("aa_permission_management.access_permission_management")
def dashboard(request: WSGIRequest) -> HttpResponse:
    """
    Render the dashboard for AA Permission Management.

    :param request:
    :type request:
    :return:
    :rtype:
    """

    return render(
        request=request,
        template_name="aa_permission_management/views/dashboard.html",
    )


@permission_required("aa_permission_management.access_permission_management")
def ajax_get_permissions(
    request: WSGIRequest, permission_type: str, element_id: int
) -> HttpResponse:
    """
    AJAX view to get permissions for a group or state.

    :param request:
    :type request:
    :param permission_type:
    :type permission_type:
    :param element_id:
    :type element_id:
    :return:
    :rtype:
    """

    if permission_type == "group":
        assigned_permissions = get_group_permissions(element_id)

        logger.debug(f"Permissions for group {element_id}: {assigned_permissions}")
    elif permission_type == "state":
        assigned_permissions = get_state_permissions(element_id)

        logger.debug(f"Permissions for state {element_id}: {assigned_permissions}")
    else:
        raise ValueError("Invalid type")

    all_permissions = get_all_permissions()
    assigned_set = (
        set(assigned_permissions) if assigned_permissions is not None else set()
    )
    available_permissions = [p for p in all_permissions if p not in assigned_set]

    context = {
        "permission_type": permission_type,
        "element_id": element_id,
        "permissions": available_permissions,
        "assigned_permissions": assigned_permissions,
    }

    return render(
        request=request,
        template_name="aa_permission_management/partials/ajax/permissions.html",
        context=context,
    )


@permission_required("aa_permission_management.access_permission_management")
def ajax_update_permissions(request: WSGIRequest) -> HttpResponse:
    """
    AJAX view to update permissions for a group or state.

    :param request:
    :type request:
    :param permission_type:
    :type permission_type:
    :param element_id:
    :type element_id:
    :return:
    :rtype:
    """

    # Validate request method
    if request.method != "POST":
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    try:
        request_body = json.loads(request.body)
        required_keys = ("permission_type", "element_id", "permissions")

        if not all(key in request_body for key in required_keys):
            raise ValueError("Missing required keys")

        permission_type = request_body["permission_type"]
        element_id = request_body["element_id"]
        permissions = set(request_body["permissions"])

        logger.debug(
            f"Parsed request body: permission_type={permission_type}, element_id={element_id}, permissions={permissions}"
        )
    except (json.JSONDecodeError, ValueError, TypeError, KeyError):
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    if permission_type == "group":
        set_group_permissions(element_id, permissions)

        return HttpResponse(content="Success", status=HTTPStatus.OK)

    if permission_type == "state":
        set_state_permissions(element_id, permissions)

        return HttpResponse(content="Success", status=HTTPStatus.OK)

    return HttpResponse(
        content="Error: Invalid Permission Type", status=HTTPStatus.NO_CONTENT
    )


class GroupsTableView(PermissionRequiredMixin, DataTablesView):
    """
    Datatables view for Auth Groups.
    """

    permission_required = "aa_permission_management.access_permission_management"
    model = AuthGroup
    columns = [
        ("group__name", "{{ row.group }}"),
        ("", "{{ row.group.user_set.count }}"),
        ("", "aa_permission_management/partials/datatables/edit-group.html"),
    ]

    logger.debug("GroupsTableView initialized with columns: %s", columns)

    def get_model_qs(
        self, request: HttpRequest, *args, **kwargs  # pylint: disable=unused-argument
    ) -> QuerySet:
        """
        Get the queryset for the model.

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        qs = self.model.objects.select_related("group")

        return qs


class StatesTableView(PermissionRequiredMixin, DataTablesView):
    """
    Datatables view for Auth Groups.
    """

    permission_required = "aa_permission_management.access_permission_management"
    model = State
    columns = [
        ("name", "{{ row.name }}"),
        ("", "{{ row.user_count }}"),
        ("", "aa_permission_management/partials/datatables/edit-state.html"),
    ]

    logger.debug("StatesTableView initialized with columns: %s", columns)

    def get_model_qs(
        self, request: HttpRequest, *args, **kwargs  # pylint: disable=unused-argument
    ) -> QuerySet:
        """
        Get the queryset for the model.

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        qs = self.model.objects.all().annotate(user_count=Count("userprofile__id"))

        return qs
