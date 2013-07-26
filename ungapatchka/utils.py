import os
import bz2
import gzip
import logging
import shutil
import sys

from itertools import takewhile, izip_longest
from csv import DictReader
from collections import Iterable, OrderedDict
from os import path

log = logging.getLogger(__name__)


def flattener(iterable):
    """
    Flatten nested iterables (not strings or dict-like objects).

    Poached from http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    """
    for el in iterable:
        if isinstance(el, Iterable) and not (isinstance(el, basestring) or hasattr(el, 'get')):
            for sub in flatten(el):
                yield sub
        else:
            yield el


def chunker(seq, size, combine_last = None):
    """
    Break sequence seq into lists of length `size`. If the length of
    the final list is < 'combine_last', it is appended to the end of
    the penultimate element.
    """

    chunks = [seq[pos:pos + size] for pos in xrange(0, len(seq), size)]
    if combine_last and len(chunks[-1]) < combine_last:
        chunks[-2].extend(chunks.pop(-1))

    return iter(chunks)


def grouper(n, iterable, pad=True):
    """
    Return sequence of n-tuples composed of successive elements of
    iterable; last tuple is padded with None if necessary. Not safe
    for iterables with None elements.
    """

    args = [iter(iterable)] * n
    iterout = izip_longest(fillvalue=None, *args)

    if pad:
        return iterout
    else:
        return (takewhile(lambda x: x is not None, c) for c in iterout)


def cast(val):
    for func in [int, float, lambda x: x.strip()]:
        try:
            return func(val)
        except ValueError:
            pass


def mkdir(dirpath, clobber = False):
    """
    Create a (potentially existing) directory without errors. Raise
    OSError if directory can't be created. If clobber is True, remove
    dirpath if it exists.
    """

    if clobber:
        shutil.rmtree(dirpath, ignore_errors = True)

    try:
        os.mkdir(dirpath)
    except OSError:
        pass

    if not path.exists(dirpath):
        raise OSError('Failed to create %s' % dirpath)

    return dirpath


def parse_extras(s, numeric = True):
    """
    Return an OrderedDict parsed from a string in the format
    "key1:val1,key2:val2"
    """

    return OrderedDict((k, cast(v) if numeric else v)
                       for k, v in [e.split(':') for e in s.split(',')])


class Opener(object):
    """Factory for creating file objects

    Keyword Arguments:
        - mode -- A string indicating how the file is to be opened. Accepts the
            same values as the builtin open() function.
        - bufsize -- The file's desired buffer size. Accepts the same values as
            the builtin open() function.
    """

    def __init__(self, mode = 'r', bufsize = -1):
        self._mode = mode
        self._bufsize = bufsize

    def __call__(self, string):
        if string is sys.stdout or string is sys.stdin:
            return string
        elif string == '-':
            return sys.stdin if 'r' in self._mode else sys.stdout
        elif string.endswith('.bz2'):
            return bz2.BZ2File(string, self._mode, self._bufsize)
        elif string.endswith('.gz'):
            return gzip.open(string, self._mode, self._bufsize)
        else:
            return open(string, self._mode, self._bufsize)

    def __repr__(self):
        args = self._mode, self._bufsize
        args_str = ', '.join(repr(arg) for arg in args if arg != -1)
        return '{}({})'.format(type(self).__name__, args_str)


def opener(pth, mode = 'r', bufsize = -1):
    return Opener(mode, bufsize)(pth)


class Csv2Dict(object):
    """Easy way to convert a csv file into a dictionary
    using the argparse type function

    Keyword Arguments:
        - index -- csv column to key index the dictionary
        - value -- csv column to value the dictionary
        - fieldnames -- csv column names
    """

    def __init__(self, index = None, value = None, *args, **kwds):
        self.index = index
        self.value = value
        self.args = args
        self.kwds = kwds

    def __call__(self, pth):
        reader = DictReader(opener(pth), *self.args, **self.kwds)

        if not self.index:
            self.index = reader.fieldnames[0]

        results = {}
        for r in reader:
            key = r.pop(self.index)
            if len(r) == 1:
                results[key] = r.popitem()[1]
            elif self.value:
                results[key] = r[self.value]
            else:
                results[key] = r

        return results


def csv2dict(pth, index, value, *args, **kwds):
    return Csv2Dict(index, value, args, kwds)(pth)
