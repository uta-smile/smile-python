"""Flags package for SMILE lab, mostly borrowed from tensorflow.app.flags."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse as _argparse
import sys

from absl import flags as absl_flags


class NamedParser(object):  # pylint: disable=too-few-public-methods
    """Parser object with name."""

    def __init__(self, name, parser):
        self.name = name
        self.parser = parser
        self._subparsers = None
        self.children = {}

    def _get_subparsers(self, dest):
        """Get named subparsers."""
        if not self._subparsers:
            self._subparsers = self.parser.add_subparsers(dest=dest)
        elif self._subparsers.dest != dest:
            raise KeyError(
                "Subparser names mismatch. You can only create one subcommand.")
        return self._subparsers

    def get_subparser(self, name, dest="subcommand", **kwargs):
        """Get or create subparser."""
        if name not in self.children:
            # Create the subparser.
            subparsers = self._get_subparsers(dest)
            parser = subparsers.add_parser(name, **kwargs)
            self.children[name] = NamedParser(name, parser)
        return self.children[name]


_GLOBAL_PARSER = NamedParser("root", _argparse.ArgumentParser())


class Subcommand(object):  # pylint: disable=too-few-public-methods
    """Subcommand Context. Provide support for subcommand."""

    DEFAULT_CONTEXT = None
    CURRENT_PARSER = _GLOBAL_PARSER

    def __init__(self, subcmd, dest="subcommand"):
        self.subcmd = subcmd
        self.dest = dest
        self._old_ctx = None
        self._old_parser = None

    def __enter__(self):
        self._old_ctx = Subcommand.DEFAULT_CONTEXT
        self._old_parser = Subcommand.CURRENT_PARSER
        Subcommand.DEFAULT_CONTEXT = self
        Subcommand.CURRENT_PARSER = self._old_parser.get_subparser(
            self.subcmd, dest=self.dest)
        return self

    def __exit__(self, ptype, value, trace):
        Subcommand.DEFAULT_CONTEXT = self._old_ctx
        Subcommand.CURRENT_PARSER = self._old_parser


Subcommand.DEFAULT_CONTEXT = Subcommand("root", "root_command")


def get_context_parser():
    """Get context parser."""
    return Subcommand.CURRENT_PARSER.parser


def get_root_parser():
    """Get root parser."""
    return _GLOBAL_PARSER.parser


class _FlagValues(object):  # pylint: disable=too-few-public-methods
    """Global container and accessor for flags and their values."""

    def __init__(self):
        self.__dict__['__flags'] = {}
        self.__dict__['__parsed'] = False

    def _parse_flags(self, args=None):
        # Use argparse to parse first.
        result, unparsed = get_root_parser().parse_known_args(args=args)
        for flag_name, val in vars(result).items():
            self.__dict__['__flags'][flag_name] = val
        self.__dict__['__parsed'] = True
        # Parse the rest flags with absl.
        unparsed = absl_flags.FLAGS(sys.argv[:1] + unparsed)
        return unparsed

    def __getattr__(self, name):
        """Retrieves the 'value' attribute of the flag --name."""
        if not self.__dict__['__parsed']:
            self._parse_flags()
        value = self.__dict__['__flags'].get(name, None)
        if value is None:
            value = getattr(absl_flags.FLAGS, name, None)
        if value is None:
            raise AttributeError(name)
        return value

    def __setattr__(self, name, value):
        """Sets the 'value' attribute of the flag --name."""
        if not self.__dict__['__parsed']:
            self._parse_flags()
        if name not in self.__dict__['__flags']:
            absl_value = getattr(absl_flags.FLAGS, name, None)
            if absl_value is not None:
                setattr(absl_flags.FLAGS, name, value)
            else:
                self.__dict__['__flags'][name] = value


def _define_helper(flag_name, default_value, docstring, flagtype, required):
    """Registers 'flag_name' with 'default_value' and 'docstring'."""
    option_name = flag_name if required else "--%s" % flag_name
    get_context_parser().add_argument(
        option_name, default=default_value, help=docstring, type=flagtype)


# Provides the global object that can be used to access flags.
FLAGS = _FlagValues()


def DEFINE_string(flag_name, default_value, docstring, required=False):  # pylint: disable=invalid-name
    """Defines a flag of type 'string'.
    Args:
        flag_name: The name of the flag as a string.
        default_value: The default value the flag should take as a string.
        docstring: A helpful message explaining the use of the flag.
    """
    _define_helper(flag_name, default_value, docstring, str, required)


def DEFINE_integer(flag_name, default_value, docstring, required=False):  # pylint: disable=invalid-name
    """Defines a flag of type 'int'.
    Args:
        flag_name: The name of the flag as a string.
        default_value: The default value the flag should take as an int.
        docstring: A helpful message explaining the use of the flag.
    """
    _define_helper(flag_name, default_value, docstring, int, required)


def DEFINE_boolean(flag_name, default_value, docstring):  # pylint: disable=invalid-name
    """Defines a flag of type 'boolean'.
    Args:
        flag_name: The name of the flag as a string.
        default_value: The default value the flag should take as a boolean.
        docstring: A helpful message explaining the use of the flag.
    """

    # Register a custom function for 'bool' so --flag=True works.
    def str2bool(bool_str):
        """Return a boolean value from a give string."""
        return bool_str.lower() in ('true', 't', '1')

    get_context_parser().add_argument(
        '--' + flag_name,
        nargs='?',
        const=True,
        help=docstring,
        default=default_value,
        type=str2bool)

    # Add negated version, stay consistent with argparse with regard to
    # dashes in flag names.
    get_context_parser().add_argument(
        '--no' + flag_name,
        action='store_false',
        dest=flag_name.replace('-', '_'))


# The internal google library defines the following alias, so we match
# the API for consistency.
DEFINE_bool = DEFINE_boolean  # pylint: disable=invalid-name


def DEFINE_float(flag_name, default_value, docstring, required=False):  # pylint: disable=invalid-name
    """Defines a flag of type 'float'.
    Args:
        flag_name: The name of the flag as a string.
        default_value: The default value the flag should take as a float.
        docstring: A helpful message explaining the use of the flag.
    """
    _define_helper(flag_name, default_value, docstring, float, required)
