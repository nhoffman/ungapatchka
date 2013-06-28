"""
Test utils module.
"""

from os import path
import unittest
import logging

from ungapatchka.utils import flattener, mkdir

from __init__ import TestBase
log = logging.getLogger(__name__)

class Args(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class TestFlatten(unittest.TestCase):
    def test01(self):
        L = [[1,2],['three',['four',5]]]
        flattener(L)
