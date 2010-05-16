# Copyright (C) 2010 Peter Teichman

import unittest

from instatrace.stats import Statistics

class testStatistics(unittest.TestCase):
    def testStats(self):
        name = "test_stat"
        s = Statistics()

        s.add_sample(name, 1)
        s.add_sample(name, 2)
        s.add_sample(name, 3)

        test_stat = s.statistics.get(name)

        self.assertEqual(name, test_stat._name)

        stats = test_stat.stats()

        self.assertEqual(3, stats.get("count"))
        self.assertEqual(6, stats.get("total"))
        self.assertAlmostEqual(2, stats.get("mean"))
        self.assertAlmostEqual(0.8164966, stats.get("stddev"))
