"""
Setup.py template. Try this:

    sed 's/pypackage/newpackagename/g;s/pypack/newscriptname/g' setup.py
"""

import os
import subprocess
import shutil
from distutils.core import setup
from os.path import join

subprocess.call('git log --pretty=format:%h -n 1 > pypackage/data/sha', shell = True)
subprocess.call('git shortlog --format="XXYYXX%h" | grep -c XXYYXX > pypackage/data/ver', shell = True)

from pypackage import __version__

params = {'author': 'Your name',
          'author_email': 'Your email',
          'description': 'Package description',
          'name': 'pypackage',
          'packages': ['pypackage','pypackage.scripts','pypackage.subcommands'],
          'package_dir': {'pypackage': 'pypackage'},
          'scripts': ['pypack'],
          'version': __version__,
          'package_data': {'pypackage': [join('data',f) for f in ['sha','ver']]}
          }
    
setup(**params)

