"""Tests for our flags implementation."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest

from smile import flags

flags.DEFINE_string("string_foo", "default_val", "HelpString")
flags.DEFINE_integer("int_foo", 42, "HelpString")
flags.DEFINE_float("float_foo", 42.0, "HelpString")

flags.DEFINE_boolean("bool_foo", True, "HelpString")
flags.DEFINE_boolean("bool_negation", True, "HelpString")
flags.DEFINE_boolean("bool-dash-negation", True, "HelpString")
flags.DEFINE_boolean("bool_a", False, "HelpString")
flags.DEFINE_boolean("bool_c", False, "HelpString")
flags.DEFINE_boolean("bool_d", True, "HelpString")
flags.DEFINE_bool("bool_e", True, "HelpString")

with flags.Subcommand("dummy_action", dest="action"):
    pass

with flags.Subcommand("move", dest="action"):
    flags.DEFINE_string("move_string", "default", "help")
    flags.DEFINE_bool("move_bool", True, "HelpString")

    with flags.Subcommand("dummy_object", dest="object"):
        pass

    with flags.Subcommand("wa", dest="object"):
        flags.DEFINE_string("move_wa_string", "default_wa", "help")
        flags.DEFINE_bool("move_wa_bool", False, "HelpString")

FLAGS = flags.FLAGS

class FlagsTest(unittest.TestCase):
    """Unit tests for flags library."""

    def setUp(self):
        """Set up function."""
        # provide the default action.
        FLAGS._parse_flags(["dummy_action"]) # pylint: disable=protected-access

    def test_string(self):
        """Test DEFINE_string."""
        self.assertEqual("default_val", FLAGS.string_foo)
        FLAGS._parse_flags(["--string_foo", "bar", "dummy_action"]) # pylint: disable=protected-access
        self.assertEqual("bar", FLAGS.string_foo)

    def test_bool(self):
        """Test DEFINE_bool."""
        self.assertTrue(FLAGS.bool_foo)
        FLAGS._parse_flags(["--nobool_foo", "dummy_action"]) # pylint: disable=protected-access
        self.assertFalse(FLAGS.bool_foo)

    def test_bool_commandlines(self):
        """Test DEFINE_bool."""
        # Specified on command line with no args, sets to True,
        # even if default is False.
        FLAGS._parse_flags([ # pylint: disable=protected-access
            "--bool_a", "--nobool_negation", "--bool_c=True", "--bool_d=False", "dummy_action"
        ])
        self.assertEqual(True, FLAGS.bool_a)

        # --no before the flag forces it to False, even if the
        # default is True
        self.assertEqual(False, FLAGS.bool_negation)

        # --bool_flag=True sets to True
        self.assertEqual(True, FLAGS.bool_c)

        # --bool_flag=False sets to False
        self.assertEqual(False, FLAGS.bool_d)

    def test_int(self):
        """Test DEFINE_integer."""
        self.assertEquals(42, FLAGS.int_foo)
        FLAGS._parse_flags(["--int_foo", "-1", "dummy_action"]) # pylint: disable=protected-access
        self.assertEquals(-1, FLAGS.int_foo)

    def test_float(self):
        """Test DEFINE_float."""
        self.assertEquals(42.0, FLAGS.float_foo)
        FLAGS._parse_flags(["--float_foo", "-1.0", "dummy_action"]) # pylint: disable=protected-access
        self.assertEquals(-1.0, FLAGS.float_foo)

    def test_subcmd(self):
        """Test subcommand action and string."""
        # test default value.
        FLAGS._parse_flags(["move", "dummy_object"]) # pylint: disable=protected-access
        self.assertEquals("move", FLAGS.action)
        self.assertEquals("default", FLAGS.move_string)
        self.assertTrue(FLAGS.move_bool)

        # test change change value via commandline.
        FLAGS._parse_flags(["move", "--move_string", "up", "--nomove_bool", "dummy_object"]) # pylint: disable=protected-access
        self.assertEquals("move", FLAGS.action)
        self.assertEquals("up", FLAGS.move_string)
        self.assertFalse(FLAGS.move_bool)

    def test_subsubcmd(self):
        """Test subsubcommand action and string."""
        # test default value.
        FLAGS._parse_flags(["move", "wa"]) # pylint: disable=protected-access
        self.assertEquals("move", FLAGS.action)
        self.assertEquals("wa", FLAGS.object)
        self.assertEquals("default", FLAGS.move_string)
        self.assertTrue(FLAGS.move_bool)
        self.assertEquals("default_wa", FLAGS.move_wa_string)
        self.assertFalse(FLAGS.move_wa_bool)

        # test change change value via commandline.
        FLAGS._parse_flags(["move", "--move_string", "up", "--nomove_bool", # pylint: disable=protected-access
                            "wa", "--move_wa_string", "haha", "--move_wa_bool"])
        self.assertEquals("move", FLAGS.action)
        self.assertEquals("up", FLAGS.move_string)
        self.assertFalse(FLAGS.move_bool)
        self.assertEquals("haha", FLAGS.move_wa_string)
        self.assertTrue(FLAGS.move_wa_bool)

    def test_with_domain(self):
        """Test with domain action."""
        with flags.Subcommand("dummy_action", dest="action"):
            # test default value.
            FLAGS._parse_flags(["move", "dummy_object"]) # pylint: disable=protected-access
            self.assertEquals("move", FLAGS.action)
            self.assertEquals("default", FLAGS.move_string)
            self.assertTrue(FLAGS.move_bool)
