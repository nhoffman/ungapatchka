import os
import gzip
import logging
import shutil
import sys

from os import path

try:
    import bz2
except ImportError as err:
    def bz2_open(filename, mode, *args, **kwargs):
        sys.exit(err)
else:
    bz2_open = bz2.open if hasattr(bz2, 'open') else bz2.BZ2File

log = logging.getLogger(__name__)


def cast(val):
    """Attempt to coerce `val` into a numeric type, or a string stripped
    of whitespace.

    """

    for func in [int, float, lambda x: x.strip(), lambda x: x]:
        try:
            return func(val)
        except ValueError:
            pass


def mkdir(dirpath, clobber=False):
    """
    Create a (potentially existing) directory without errors. Raise
    OSError if directory can't be created. If clobber is True, remove
    dirpath if it exists.
    """

    if clobber:
        shutil.rmtree(dirpath, ignore_errors=True)

    try:
        os.mkdir(dirpath)
    except OSError:
        pass

    if not path.exists(dirpath):
        raise OSError('Failed to create %s' % dirpath)

    return dirpath


class Opener(object):
    """Factory for creating file objects. Transparenty opens compressed
    files for reading or writing based on suffix (.gz and .bz2 only).

    Example::

        with Opener()('in.txt') as infile, Opener('w')('out.gz') as outfile:
            outfile.write(infile.read())
    """

    def __init__(self, mode='r', *args, **kwargs):
        self.mode = mode
        self.args = args
        self.kwargs = kwargs
        self.writable = 'w' in self.mode

    def __call__(self, obj):
        if obj is sys.stdout or obj is sys.stdin:
            return obj
        elif obj == '-':
            return sys.stdout if self.writable else sys.stdin
        else:
            openers = {'bz2': bz2_open, 'gz': gzip.open}
            __, suffix = obj.rsplit('.', 1)
            # in python3, both bz2 and gz libraries default to binary input and output
            mode = self.mode
            if sys.version_info.major == 3 and suffix in openers \
               and mode in {'w', 'r'}:
                mode += 't'
            opener = openers.get(suffix, open)
            return opener(obj, mode=mode, *self.args, **self.kwargs)
