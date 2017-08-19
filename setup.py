import glob
import os
import subprocess

from distutils.core import Command
from setuptools import setup, find_packages

subprocess.call(
    ('mkdir -p ungapatchka/data && '
     'git describe --tags --dirty > ungapatchka/data/ver.tmp '
     '&& mv ungapatchka/data/ver.tmp ungapatchka/data/ver '
     '|| rm -f ungapatchka/data/ver.tmp'),
    shell=True, stderr=open(os.devnull, "w"))

from ungapatchka import __version__


class CheckVersion(Command):
    description = 'Confirm that the stored package version is correct'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        with open('ungapatchka/data/ver') as f:
            stored_version = f.read().strip()

        git_version = subprocess.check_output(
            ['git', 'describe', '--tags', '--dirty']).strip()

        assert stored_version == git_version
        print('the current version is', stored_version)


package_data = ['data/*']

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
          'test_suite': 'tests',
          'cmdclass': {'check_version': CheckVersion}
          }

setup(**params)
