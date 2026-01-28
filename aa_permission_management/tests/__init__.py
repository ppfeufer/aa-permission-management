"""
Initializing our tests
"""

# Standard Library
import socket

# Django
from django.test import TestCase

# AA Permission Management
from aa_permission_management.tests.fixtures.utils import create_fake_user


class SocketAccessError(Exception):
    """
    Error raised when a test script accesses the network
    """


class BaseTestCase(TestCase):
    """
    Variation of Django's TestCase class that prevents any network use.

    Example:

        .. code-block:: python

            class TestMyStuff(BaseTestCase):
                def test_should_do_what_i_need(self): ...

    """

    @classmethod
    def setUpClass(cls):
        """
        Sets up the class by replacing the socket.socket method with a guard that raises an error on network access.

        :return:
        :rtype:
        """

        cls.socket_original = socket.socket

        socket.socket = cls.guard

        return super().setUpClass()

    def setUp(self):
        """
        Sets up the test case by ensuring the socket.socket method is still the guard.

        :return:
        :rtype:
        """

        super().setUp()

        self.user_with_permission = create_fake_user(
            character_id=10001,
            character_name="Jean Luc Picard",
            permissions=["aa_permission_management.access_permission_management"],
        )
        self.user_without_permission = create_fake_user(
            character_id=10002,
            character_name="Wesley Crusher",
        )

    @classmethod
    def tearDownClass(cls):
        """
        Restores the original socket.socket method after tests are done.

        :return:
        :rtype:
        """

        socket.socket = cls.socket_original

        return super().tearDownClass()

    @staticmethod
    def guard(*args, **kwargs):
        """
        Guard method that raises a SocketAccessError when network access is attempted.

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        raise SocketAccessError("Attempted to access network")
