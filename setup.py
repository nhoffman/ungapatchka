import glob
import os
import subprocess

from setuptools import setup, find_packages

subprocess.call(
    ('git describe --tags --dirty > ungapatchka/data/ver.tmp'
     '&& mv ungapatchka/data/ver.tmp ungapatchka/data/ver '
     '|| rm -f ungapatchka/data/ver.tmp'),
    shell=True, stderr=open(os.devnull, "w"))

from ungapatchka import __version__
package_data = glob.glob('data/*')

params = {'author': 'Your name',
          'author_email': 'Your email',
          'description': 'Package description',
          'name': 'ungapatchka',
          'packages': find_packages(),
          'package_dir': {'ungapatchka': 'ungapatchka'},
          'entry_points': {
              'console_scripts': ['kapow = ungapatchka.scripts.main:main']
          },
          'version': __version__,
          'package_data': {'ungapatchka': package_data},
          'test_suite': 'tests'
          }

setup(**params)
