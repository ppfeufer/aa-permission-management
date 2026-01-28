"""
URL config
"""

# Django
from django.urls import include, path

# AA Permission Management
from aa_permission_management import views
from aa_permission_management.constants import INTERNAL_URL_PREFIX

app_name: str = "aa_permission_management"  # pylint: disable=invalid-name

ajax_urls = [
    path(route="get-groups/", view=views.GroupsTableView.as_view(), name="get_groups"),
    path(route="get-states/", view=views.StatesTableView.as_view(), name="get_states"),
]

urlpatterns = [
    path(route="", view=views.dashboard, name="dashboard"),
    # Ajax calls urls
    path(route=f"{INTERNAL_URL_PREFIX}/ajax/", view=include(ajax_urls)),
]
