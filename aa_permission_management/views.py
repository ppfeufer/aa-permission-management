"""
Views for the AA Permission Management app.
"""

# Django
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.shortcuts import render

# Alliance Auth
from allianceauth.authentication.models import State
from allianceauth.framework.datatables import DataTablesView
from allianceauth.groupmanagement.models import AuthGroup
from allianceauth.services.hooks import get_extension_logger

# AA Permission Management
from aa_permission_management import __title__
from aa_permission_management.providers import AppLogger

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


@permission_required("aa_permission_management.access_permission_management")
def dashboard(request):
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


class GroupsTableView(PermissionRequiredMixin, DataTablesView):
    """
    Datatables view for Auth Groups.
    """

    permission_required = "aa_permission_management.access_permission_management"
    model = AuthGroup
    columns = [
        ("group__name", "{{ row.group }}"),
        ("", "{{ row.group.user_set.count }}"),
        ("", "{{ row.get_permissions_display|safe }}"),
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
        ("", "{{ row.get_permissions_display|safe }}"),
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
