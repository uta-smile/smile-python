"""Generic entry point script. Idea from tensorflow."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

from smile import flags


def run(main=None, argv=None):
    """Runs the program with an optional 'main' function and 'argv' list."""
    flags_obj = flags.FLAGS

    # Extract the args from the optional `argv` list.
    args = argv[1:] if argv else None

    # Parse the known flags from that list, or from the command
    # line otherwise.
    # pylint: disable=protected-access
    flags_passthrough = flags_obj._parse_flags(args=args)
    # pylint: enable=protected-access

    main = main or sys.modules['__main__'].main

    # Call the main function, passing through any arguments
    # to the final program.
    sys.exit(main(sys.argv[:1] + flags_passthrough))
