"""
Auth hooks
"""

# Django
from django.core.handlers.wsgi import WSGIRequest

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Permission Management
from aa_permission_management import __title_translated__, urls


class PermissionManagementMenuItem(
    MenuItemHook
):  # pylint: disable=too-few-public-methods
    """
    This class ensures only authorized users will see the menu entry
    """

    def __init__(self) -> None:
        """
        Initialize menu item
        """
        MenuItemHook.__init__(
            self,
            text=__title_translated__,
            classes="fa-solid fa-list-check",
            url_name="aa_permission_management:dashboard",
            navactive=["aa_permission_management:"],
        )

    def render(self, request: WSGIRequest) -> str:
        """
        Render app pages

        :param request: WSGIRequest
        :return: HTML string
        """

        if request.user.has_perm(
            "aa_permission_management.access_permission_management"
        ):
            return MenuItemHook.render(self, request=request)

        return ""


@hooks.register("menu_item_hook")
def register_menu() -> MenuItemHook:
    """
    Register our menu

    :return: MenuItemHook
    """

    return PermissionManagementMenuItem()


@hooks.register("url_hook")
def register_urls() -> UrlHook:
    """
    Register our urls

    :return: UrlHook
    """

    return UrlHook(
        urls=urls,
        namespace="aa_permission_management",
        base_url="^permission-management/",
    )
