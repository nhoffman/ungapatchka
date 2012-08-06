"""
Test subcommands.
"""

import os
import unittest
import logging
import pprint
import sys

from pypackage.scripts.main import main
from pypackage.subcommands import subcommand_template

from __init__ import TestCaseSuppressOutput, TestBase
import __init__ as config
log = logging.getLogger(__name__)
                        
class TestTemplate(TestCaseSuppressOutput, TestBase):
    
    def testExit01(self):
        self.assertRaises(SystemExit, main, ['notacommand'])

    def testExit02(self):
        self.assertRaises(SystemExit, main, ['-h'])

    def test01(self):
        main(['subcommand_template', 'infile', 'outfile', '--monkey-type', 'macaque'])
        
