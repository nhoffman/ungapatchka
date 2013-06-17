======================================
ungapatchka: a python package template
======================================

ungapatchka
    Yiddish word that describes the overly ornate, busy, ridiculously
    over-decorated, and garnished to the point of
    distaste. (www.urbandictionary.com/define.php?term=ungapatchka)

.. contents:: Table of Contents

why?
====

* Provides a basic package framework including a CLI using ``argparse`` that divides functionality into subcommands (à la git, apt-get, etc)
* The CLI entry point imports the local version of the python package when it is invoked using an absolute or relative path (see below).
* Provides some useful utilities, for example ``utils.Opener`` as a replacement for ``argparse.FileType``

dependencies
============

* Python 2.7.x
* Tested on Linux and OS X.

installation
============

Clone the project from the git repository to create a new
project. You will need to choose a name for the project (let's say
"myproject"), and for the main script ("runme")::

    $ git clone git://github.com/nhoffman/ungapatchka.git myproject
    $ cd myproject && dev/setup.sh myproject runme

Kaopw! A new project with a new git repo::

    $ git --no-pager log -n 1
    commit 06a5280d89dc47f6a613488a96d244f4267f6b42
    Author: Noah Hoffman
    Date:   Mon Aug 6 22:46:46 2012 -0700

	first commit
    $ ./runme --version
    0001.06a5280

Now installation can be performed using ``distutils`` (which has no
dependencies outside the Python standard library)::

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
    ├── kapow
    ├── ungapatchka
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

* ``dev`` - development tools not essential for the primary functionality of the application.
* ``doc`` - files related to project documentation.
* ``ungapatchka`` - the Python package implementing most of the project functionality. This subdirectory is installed to the system.
* ``testfiles`` - files and data used for testing.
* ``tests`` - subpackage implementing unit tests.

Note that ``kapow`` and ``ungapatchka`` are placeholder names that are replaced with your script and project names during setup.

execution
=========

The ``kapow`` script provides the user interface, and uses standard
UNIX command line syntax. Note that for development, it is convenient
to run ``kapow`` from within the project directory by specifying the
relative path to the script::

    % cd ungapatchka
    % ./kapow --help

or::

   % path/to/ungapatchka/kapow --help

When invoked this way, the local version of the package is imported,
even if the version of the package is installed to the system. This is
very handy for development, and can avoid the requirement for a
virtualenv in many cases.

Commands are constructed as follows. Every command starts with the
name of the script, followed by an "action" followed by a series of
required or optional "arguments". The name of the script, the action,
and options and their arguments are entered on the command line
separated by spaces. Help text is available for both the ``kapow``
script and individual actions using the ``-h`` or ``--help`` options.

versions
========

We use abbrevited git sha hashes to identify the software version::

    % ./kapow -V
    0128.9790c13

The version information is saved in ``ungapatchka/data`` when ``setup.py``
is run (on installation, or even by executing ``python setup.py
-h``).

unit tests
==========

Unit tests are implemented using the ``unittest`` module in the Python
standard library. The ``tests`` subdirectory is itself a Python
package that imports the local version (ie, the version in the project
directory, not the version installed to the system) of the
package. All unit tests can be run like this::

    % ./testall
    ...........
    ----------------------------------------------------------------------
    Ran 11 tests in 0.059s

    OK

A single unit test can be run by referring to a specific module,
class, or method within the ``tests`` package using dot notation::

    % ./testone -v tests.test_utils
    test01 (tests.test_utils.TestFlatten) ... ok
    test01 (tests.test_utils.TestGetOutfile) ... ok
    test02 (tests.test_utils.TestGetOutfile) ... ok
    test03 (tests.test_utils.TestGetOutfile) ... ok
    test04 (tests.test_utils.TestGetOutfile) ... ok
    test05 (tests.test_utils.TestGetOutfile) ... ok
    test06 (tests.test_utils.TestGetOutfile) ... ok
    test07 (tests.test_utils.TestGetOutfile) ... ok

    ----------------------------------------------------------------------
    Ran 8 tests in 0.046s

    OK

license
=======

Copyright (c) 2012 Noah Hoffman

Released under the MIT License:

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
