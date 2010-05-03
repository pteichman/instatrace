# Copyright (C) 2010 Peter Teichman

import unittest

from instatrace.stats import Statistic

class testStatistic(unittest.TestCase):
    def testName(self):
        name = "test_stat"
        s = Statistic(name, [])

        self.assertEqual(name, s.name)
