"""Test helper for smoke_test.sh."""

# Similar to https://github.com/abseil/abseil-py/blob/master/smoke_tests/smoke_test.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import smile as sm
from smile import flags
from smile import logging

flags.DEFINE_string("param", "default_value", "some help infomation")

FLAGS = flags.FLAGS


def main(_):
    """Print out the FLAGS in the main function."""
    logging.info("param = %s", FLAGS.param)


if __name__ == "__main__":
    sm.app.run()
