import unittest

# import our test modules
from . import stats

__all__ = ["suite"]

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(stats))
