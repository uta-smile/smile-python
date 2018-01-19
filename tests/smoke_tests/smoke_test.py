"""Test helper for smoke_test.sh."""

# Similar to https://github.com/abseil/abseil-py/blob/master/smoke_tests/smoke_test.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import smile as sm
from smile import flags
from smile import logging

flags.DEFINE_string("param", "default_value", "A general flag.")

with flags.Subcommand("echo", dest="action"):
    flags.DEFINE_string("echo_text", "", "The text to be echoed out.")

with flags.Subcommand("echo_bool", dest="action"):
    flags.DEFINE_bool("just_do_it", False, "some help infomation")

FLAGS = flags.FLAGS


def main(_):
    """Print out the FLAGS in the main function."""
    logging.info("param = %s", FLAGS.param)
    if FLAGS.action == "echo":
        logging.warning(FLAGS.echo_text)
    elif FLAGS.action == "echo_bool":
        logging.info("Just do it? %s", "Yes!" if FLAGS.just_do_it else "No :(")


if __name__ == "__main__":
    sm.app.run()
