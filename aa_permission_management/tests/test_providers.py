"""
Test cases for the permission management providers in the aa_permission_management module.
"""

# Standard Library
import logging

# AA Permission Management
from aa_permission_management.providers import AppLogger
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
        app_logger = AppLogger(logger, "PREFIX")
        message, kwargs = app_logger.process("Test message", {})

        self.assertEqual(message, "[PREFIX] Test message")

    def test_handles_empty_prefix_correctly(self):
        """
        Test that the AppLogger correctly handles an empty prefix.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger, "")
        message, kwargs = app_logger.process("Test message", {})

        self.assertEqual(message, "[] Test message")

    def test_preserves_kwargs_correctly(self):
        """
        Test that the AppLogger preserves keyword arguments correctly.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger, "PREFIX")
        message, kwargs = app_logger.process("Test message", {"key": "value"})

        self.assertEqual(kwargs, {"key": "value"})

    def test_handles_non_string_message_correctly(self):
        """
        Test that the AppLogger correctly handles non-string messages.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger, "PREFIX")
        message, kwargs = app_logger.process(12345, {})

        self.assertEqual(message, "[PREFIX] 12345")

    def test_handles_none_prefix_correctly(self):
        """
        Test that the AppLogger correctly handles a None prefix.

        :return:
        :rtype:
        """

        logger = logging.getLogger("test_logger")
        app_logger = AppLogger(logger, None)
        message, kwargs = app_logger.process("Test message", {})

        self.assertEqual(message, "[None] Test message")
