"""
Models for the Permission Management app
"""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


class General(models.Model):
    """
    Meta model for app permissions
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class
        """

        managed = False
        default_permissions = ()
        permissions = (
            (
                "access_permission_management",
                _("Can access the Permission Management module and manage permissions"),
            ),
        )
        verbose_name = _("Permission Management")
