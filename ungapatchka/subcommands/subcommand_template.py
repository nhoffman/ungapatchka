"""Template for a subcommand.

The first line above is shown in the top-level help.  Additional lines
in this docstring are included in the help message for the subcommand.
"""

import subprocess
import tempfile
import logging
import shutil
import os

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', 
        help='A required input file')
    parser.add_argument('outfile', 
        help='A required output file')

    parser.add_argument('-m','--monkey-type',
        action='store', default='rhesus',
        help="specify type of monkey [%(default)s]")

def action(args):

    print 'monkey type:', args.monkey_type
