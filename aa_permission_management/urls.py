"""
URL config
"""

# Django
from django.urls import path

# AA Permission Management
from aa_permission_management import views

app_name: str = "aa_permission_management"  # pylint: disable=invalid-name

urlpatterns = [path(route="", view=views.dashboard, name="dashboard")]
