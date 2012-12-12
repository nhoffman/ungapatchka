"""
Assembles subcommands and provides top-level script.
"""

import argparse
from argparse import RawDescriptionHelpFormatter
from collections import defaultdict
import logging
import pkgutil
import sys
from importlib import import_module
from ungapatchka import subcommands, __version__ as version, __doc__ as docstring

def main(argv):
    action, arguments = parse_arguments(argv)

    loglevel = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }.get(arguments.verbosity, logging.DEBUG)

    if arguments.verbosity > 1:
        logformat = '%(levelname)s %(module)s %(lineno)s %(message)s'
    else:
        logformat = '%(message)s'

    # set up logging
    logging.basicConfig(file=sys.stdout, format=logformat, level=loglevel)

    return action(arguments)

def parse_arguments(argv):
    """
    Create the argument parser
    """

    parser = argparse.ArgumentParser(description=docstring)

    parser.add_argument('-V', '--version', action='version',
        version = version,
        help = 'Print the version number and exit')

    parser.add_argument('-v', '--verbose',
        action='count', dest='verbosity', default=1,
        help='Increase verbosity of screen output (eg, -v is verbose, '
             '-vv more so)')
    parser.add_argument('-q', '--quiet',
        action='store_const', dest='verbosity', const=0,
        help='Suppress output')

    ##########################
    # Setup all sub-commands #
    ##########################

    subparsers = parser.add_subparsers(dest='subparser_name')

    # Begin help sub-command
    parser_help = subparsers.add_parser(
        'help', help='Detailed help for actions using `help <action>`')
    parser_help.add_argument('action', nargs=1)
    # End help sub-command

    # Organize submodules by argv
    run_action = defaultdict(list)
    for _, name, _ in pkgutil.iter_modules(subcommands.__path__):
        run_action[name in argv].append(name)

    actions = {}

    for name in run_action[True] or run_action[False]:
        # set up subcommand help text. The first line of the dosctring
        # in the module is displayed as the help text in the
        # script-level help message (`script -h`). The entire
        # docstring is displayed in the help message for the
        # individual subcommand ((`script action -h`))
        # if no individual subcommand is specified (run_action[False]),
        # a full list of docstrings is displayed
        mod = import_module('{}.{}'.format(subcommands.__name__, name))
        subparser = subparsers.add_parser(name,
                                          help = mod.__doc__.lstrip().split('\n', 1)[0],
                                          description = mod.__doc__,
                                          formatter_class = RawDescriptionHelpFormatter)
        mod.build_parser(subparser)
        actions[name] = mod.action
    # Determine we have called ourself (e.g. "help <action>")
    # Set arguments to display help if parameter is set
    #           *or*
    # Set arguments to perform an action with any specified options.
    arguments = parser.parse_args(argv)
    # Determine which action is in play.
    action = arguments.subparser_name

    # Support help <action> by simply having this function call itself and
    # translate the arguments into something that argparse can work with.
    if action == 'help':
        return parse_arguments([str(arguments.action[0]), '-h'])

    return actions[action], arguments
