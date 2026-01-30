"""
Views for the AA Permission Management app.
"""

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
    request: WSGIRequest, permission_type: str, permission_id: int
) -> HttpResponse:
    """
    AJAX view to get permissions for a group or state.

    :param request:
    :type request:
    :param permission_type:
    :type permission_type:
    :param permission_id:
    :type permission_id:
    :return:
    :rtype:
    """

    if permission_type == "group":
        permissions = get_group_permissions(permission_id)
    elif permission_type == "state":
        permissions = get_state_permissions(permission_id)
    else:
        raise ValueError("Invalid type")

    context = {
        "permissions": get_all_permissions(),
        "assigned_permissions": permissions,
    }

    return render(
        request=request,
        template_name="aa_permission_management/partials/ajax/permissions.html",
        context=context,
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
