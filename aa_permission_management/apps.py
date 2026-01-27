"""
App config
"""

# Django
from django.apps import AppConfig
from django.utils.text import format_lazy

# AA Permission Management
from aa_permission_management import __title_translated__, __version__


class PermissionManagementConfig(AppConfig):
    """
    Application config
    """

    name = "aa_permission_management"
    label = "aa_permission_management"
    verbose_name = format_lazy(
        "{app_title} v{version}", app_title=__title_translated__, version=__version__
    )
