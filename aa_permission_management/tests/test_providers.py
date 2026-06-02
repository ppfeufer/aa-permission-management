"""
Test cases for the permission management providers in the aa_permission_management module.
"""

# Standard Library
import logging

# AA Permission Management
from aa_permission_management import __title__
from aa_permission_management.providers.applogger import AppLogger
from aa_permission_management.tests import BaseTestCase


class TestAppLogger(BaseTestCase):
    """
    Tests for the AppLogger provider.
    """

    def test_adds_prefix_to_message_correctly(self):
        """
        Test that the AppLogger correctly adds the prefix to log messages.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger)
        message, kwargs = app_logger.process("Test message", {})

        self.assertEqual(message, f"[{__title__}] Test message")

    def test_preserves_kwargs_correctly(self):
        """
        Test that the AppLogger preserves keyword arguments correctly.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger)
        message, kwargs = app_logger.process("Test message", {"key": "value"})

        self.assertEqual(kwargs, {"key": "value"})
