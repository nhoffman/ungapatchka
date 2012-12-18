#!/usr/bin/env python

"""
Usage insreadofsed.py pattern repl file1 [file2 file3 ...]

Replace string `pattern` with repl in each file 
"""

import fileinput
import sys
import re

def main():
    pattern, repl = sys.argv[1:3]
    for line in fileinput.input(sys.argv[3:], inplace = True):
        sys.stdout.write(line.replace(pattern, repl))
    
main()
