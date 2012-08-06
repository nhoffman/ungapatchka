==========================================================
pypackage: a python package template
==========================================================

.. contents:: Table of Contents

dependencies
============

* Python 2.7.x
* A UNIX-like operating system (Linux, OS X). Not tested on Windows.

installation
============

Clone the project from the git repository::

    cd ~/src
    git clone git@url-to-repo/opiates.git
    cd opiates

Now installation can be performed using the familiar mechanism
provided by ``distutils`` (which has no dependencies outside the
Python standard library)::

    sudo python setup.py install

or using ``pip`` (which must be installed separately)::

    sudo pip install .

Subsequent (re)installation with pip should be performed using the
``-U`` option::

    sudo pip install -U .

architecture
============

This project has the following structure::

    % tree
    .
    ├── dev
    │   └── README.rst
    ├── doc
    │   └── README.rst
    ├── LICENSE.txt
    ├── pypack
    ├── pypackage
    │   ├── __init__.py
    │   ├── scripts
    │   │   ├── __init__.py
    │   │   └── main.py
    │   ├── subcommands
    │   │   ├── __init__.py
    │   │   └── subcommand_template.py
    │   └── utils.py
    ├── README.rst
    ├── setup.py
    ├── testall
    ├── testfiles
    │   └── README.rst
    ├── testone
    └── tests
	├── __init__.py
	├── test_subcommands.py
	└── test_utils.py

with contents as follows:

* ``dev`` - development tools not essential for the primary
   functionality of the application.
* ``doc`` - files related to project documentation.
* ``pypackage`` - the Python package implementing most of the project
   functionality. This subdirectory is installed to the system. You
   will want to rename this.
* ``testfiles`` - files and data used for testing.
* ``tests`` - subpackage implementing unit tests.

versions
========

We use abbrevited git sha hashes to identify the software version::

    % ./pypack -V
    0128.9790c13

The version information is saved in ``pypackage/data`` when ``setup.py``
is run (on installation, or even by executing ``python setup.py
-h``). By default the version number appears in the name of the output
file.

execution
=========

The ``pypack`` script provides the user interface, and uses standard
UNIX command line syntax. Note that for development, it is convenient
to run ``pypack`` from within the project directory by specifying the
relative path to the script::

    % ./pypack

Commands are constructed as follows. Every command starts with the
name of the script, followed by an "action" followed by a series of
required or optional "arguments". The name of the script, the action,
and options and their arguments are entered on the command line
separated by spaces. Help text is available for both the ``pypack``
script and individual actions using the ``-h`` or ``--help`` options::

unit tests
==========

Unit tests are implemented using the ``unittest`` module in the Python
standard library. The ``tests`` subdirectory is itself a Python
package that imports the local version (ie, the version in the project
directory, not the version installed to the system) of the
package. All unit tests can be run like this::

    % ./testall

A single unit test can be run by referring to a specific module,
class, or method within the ``tests`` package using dot notation::

    % ./testone tests.test_module.TestClass.test_method

license
=======

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The GLPv3 license is reproduced in LICENSE.txt

Copyright (C) 2012 Noah. G Hoffman
