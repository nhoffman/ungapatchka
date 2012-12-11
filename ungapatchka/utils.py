import os
import bz2
import gzip
import logging
import operator
import shutil
import sys
import time

from itertools import chain, takewhile, izip_longest
from csv import DictReader
from collections import Iterable, OrderedDict
from os import path

from __init__ import __version__

log = logging.getLogger(__name__)

def flatten(seq):
    """
    Poached from http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python

    Don't flatten strings or dict-like objects.
    """
    for el in seq:
        if isinstance(el, Iterable) and not (isinstance(el, basestring) or hasattr(el, 'get')):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def chunker(seq, size, combine_last = None):
    """
    Break sequence seq into lists of length `sise`. If the length of
    the final list is < 'combine_last', it is appended to the end of the
    penultimate element.
    """

    chunks = [seq[pos:pos + size] for pos in xrange(0, len(seq), size)]
    if combine_last and len(chunks[-1]) < combine_last:
        chunks[-2].extend(chunks.pop(-1))

    return iter(chunks)

def get_outfile(args, label = None, ext = None, include_version = True):
    """
    Return a file-like object open for writing. `args` is expected to
    have attributes 'infile' (None or a string specifying a file
    path), 'outfile' (None or a file-like object open for writing),
    and 'outdir' (None or a string defining a dir-path). If
    `args.outfilr` is None, the name of the outfile is derived from
    the basename of `args.infile` and is written either in the same
    directory or in `args.outdir` if provided.
    """

    version = __version__ if include_version else None

    if args.outfile is None:
        dirname, basename = path.split(args.infile)
        parts = filter(lambda x: x,
                       [path.splitext(basename)[0], version, label, ext])
        outname = path.join(args.outdir or dirname,
                            '.'.join(parts))
        if path.abspath(outname) == path.abspath(args.infile):
            raise OSError('Input and output file names are identical')
        outfile = open(outname, 'w')
    else:
        outfile = args.outfile
        if not (hasattr(outfile, 'write') and not outfile.closed and 'w' in outfile.mode):
            raise OSError('`args.outfile` must be a file-like object open for writing')

    log.debug(outfile)
    return outfile

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

def to_ascii(nums):
    """
    Encode a list of integers as an ascii string. Max allowed value is
    126-48 = 78 (avoids many special characters that might cause
    trouble). The purpose of this encoding is to store run-length
    encodings, so we're asuming that values > 78 are not plausible.
    """

    if max(nums) > 78:
        raise ValueError('values over 78 are not allowed')

    return ''.join([chr(i+48) for i in nums])

def from_ascii(chars):
    """
    Decode an ascii-encoded list of integers.
    """
    return [ord(c)-48 for c in chars]

def cast(val):
    for func in [int, float, lambda x: x.strip()]:
        try:
            return func(val)
        except ValueError:
            pass

def parse_extras(s, numeric = True):
    """
    Return an OrderedDict parsed from a string in the format
    "key1:val1,key2:val2"
    """

    return OrderedDict((k, cast(v) if numeric else v) for k,v in [e.split(':') for e in s.split(',')])

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
    """Easy way to convert a csv file into a dictionary using the argparse type function

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

def dedup(strings, comp='contains', chunksize=None):

    """
    Given a sequence of strings, return a dictionary mapping
    superstrings to substrings.

    Input
    =====

     * strings - a tuple of N strings
     * comp - defines string comparison method:

       * 'contains' -> "s1 in s2" or
       * 'eq' -> "s1 == s2"

     * chunksize - an integer defining size of partitions into which
       strings are divided; each partition is coalesced individually,
       and the results of each are merged.

    Output
    ======

     * A dict mapping superrstrings to substrings, in which keys and
     values are indices into strings.

    """

    nstrings = len(strings)

    if not chunksize:
        chunksize = nstrings

    chunks = grouper(n=chunksize, iterable=xrange(nstrings), pad=False)
    # TODO: parallelize me
    coalesced = [coalesce(strings, idx=list(c), comp=comp) for c in chunks]

    cycle = 1
    while len(coalesced) > 1:
        log.warning('merge cycle %s, %s chunks' % (cycle,len(coalesced)))
        # TODO: parallelize me
        coalesced = [merge(strings, d1, d2, comp=comp) for d1,d2 in grouper(n=2, iterable=coalesced)]
        cycle += 1

    d = coalesced[0]

    assert set(flatten(d)) == set(range(nstrings))

    return d

def grouper(n, iterable, pad=True):
    """
    Return sequence of n-tuples composed of successive elements
    of iterable; last tuple is padded with None if necessary. Not safe
    for iterables with None elements.
    """

    args = [iter(iterable)] * n
    iterout = izip_longest(fillvalue=None, *args)

    if pad:
        return iterout
    else:
        return (takewhile(lambda x: x is not None, c) for c in iterout)

def coalesce(strings, idx=None, comp='contains', log=log):

    """
    Groups a collection of strings by identifying the longest string
    representing each nested set of substrings (if comp='contains') or
    into sets of identical strings (if comp='eq')

    Input
    =====

     * strings - a tuple of N strings
     * comp - 'contains' (default) or 'eq'
     * log - a logging object; defualt is the root logger

     Output
     ======

     * a dict keyed by indices in strings. Each key i returns a list of
       indices corresponding to strings nested within (or identical to) the
       string at strings[i].
    """

    start = time.time()

    try:
        len(strings)
    except TypeError:
        strings = list(strings)

    if not idx:
        idx = range(len(strings))

    # sort idx by length, descending
    idx.sort(key=lambda i: len(strings[i]),reverse=True)
    log.debug('sort completed at %s secs' % (time.time()-start))
    nstrings = len(idx)

    d = dict((i,list()) for i in idx)

    # operator.eq(a,b) <==> a == b
    # operator.contains(a,b) <==> b in a
    compfun = getattr(operator, comp)

    while len(idx) > 0:
        parent_i = idx.pop(0)
        parent_str = strings[parent_i]
        children = set(i for i in idx if compfun(parent_str,strings[i]))
        d[parent_i].extend(children)
        idx = [x for x in idx if x not in children]

    for i in chain(*d.values()):
        del d[i]

    log.info('Coalesce %s strings to %s in %.2f secs' % (nstrings, len(d), time.time()-start))

    return d

def merge(strings, d1, d2=None, comp='contains'):

    """
    Merge two dictionaries mapping superstrings to substrings.

    Input
    =====

     * strings - a tuple of N strings
     * d1, d2 - output of coalesce()
     * comp - type of string comparison, passed to coalesce ("contains" or "eq")

    Output
    ======

     * a single dict mapping superstrings to substrings

    """

    if d2 is None:
        log.warning('d2 not provided, returning d1')
        return d1

    d = coalesce(strings, idx=d1.keys()+d2.keys(), comp=comp)

    for i, dvals in d.items():
        if dvals:
            d[i].extend(list(chain(*[d1.get(j,[]) for j in dvals])))
            d[i].extend(list(chain(*[d2.get(j,[]) for j in dvals])))
        d[i].extend(d1.get(i,[]))
        d[i].extend(d2.get(i,[]))

    if __debug__:
        d1Flat, d2Flat, dFlat = flatten(d1), flatten(d2), flatten(d)
        log.info('checking d of length %s with min,max=%s,%s' % \
            (len(d),min(dFlat),max(dFlat)))

        assert set(d1Flat + d2Flat) == set(dFlat)

        for parent, children in d.items():
            for child in children:
                assert strings[child] in strings[parent]

    return d

def org_table(rows, fieldnames, formats = None):
    """
    Format tabular data for org-mode. Rows is an iterable of
    dicts. Formats is a dict mapping a subset of fieldnames to format
    strings, eg {'name': '%s', 'height': '%.1f cm'}
    """

    fmt = formats or {}
    print '|%s|' % '|'.join(fieldnames)
    print '|%s|' % '+'.join('-'*len(k) for k in fieldnames)

    for row in rows:
        print '|%s|' % '|'.join(fmt.get(k, '%s') % row[k] for k in fieldnames)
