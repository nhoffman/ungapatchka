"""
Setup.py template. Try this:

    sed 's/ungapatchka/newpackagename/g;s/kapow/newscriptname/g' setup.py
"""

import os
import subprocess
import shutil
# from distutils.core import setup
from setuptools import setup
from os.path import join

subprocess.call('git log --pretty=format:%h -n 1 > ungapatchka/data/sha', shell = True)
subprocess.call('git shortlog --format="XXYYXX%h" | grep -c XXYYXX > ungapatchka/data/ver', shell = True)

from ungapatchka import __version__

params = {'author': 'Your name',
          'author_email': 'Your email',
          'description': 'Package description',
          'name': 'ungapatchka',
          'packages': ['ungapatchka','ungapatchka.scripts','ungapatchka.subcommands'],
          'package_dir': {'ungapatchka': 'ungapatchka'},
          'scripts': ['kapow'],
          'version': __version__,
          'package_data': {'ungapatchka': [join('data',f) for f in ['sha','ver']]},
          'test_suite': 'tests'
          }

setup(**params)
