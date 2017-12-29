from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest

from smile import logging


class FlagsTest(unittest.TestCase):
    """Unit tests for logging library."""

    def test_integration_log(self):
        """This test simply should not return any error."""
        logging.info("This is a info test message.")
        logging.warning("This is a warning test message.")
        logging.error("This is an error message.")
        logging.log(logging.INFO, "This is just another info test message.")
        logging.debug("This is a debug test message.")
        # TODO(XericZephyr@): Figure out how to test fatal logging.
