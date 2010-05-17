# Copyright (C) 2010 Peter Teichman

from ConfigParser import SafeConfigParser
import unittest

from instatrace.stats import Accumulator, Statistic

class testAccumulator(unittest.TestCase):
    def testAddSample(self):
        name1 = "stat1"
        name2 = "stat2"

        s = Accumulator()
        s.add_sample(name1, 1)
        s.add_sample(name1, 2)
        s.add_sample(name1, 3)

        s.add_sample(name2, 1)
        s.add_sample(name2, 2)
        s.add_sample(name2, 3)

        self.assertEquals([1, 2, 3], s.statistics.get(name1))
        self.assertEquals([1, 2, 3], s.statistics.get(name2))

class testStatistics(unittest.TestCase):
    def setUp(self):
        self.config = SafeConfigParser({"layout": "exponential",
                                        "scale": "1"})

    def tearDown(self):
        self.config = None

    def testStats(self):
        name = "test_stat"

        test_stat = Statistic(name, [1, 2, 3], self.config)

        self.assertEqual(name, test_stat._name)

        stats = test_stat.stats()

        self.assertEqual(3, stats.get("count"))
        self.assertEqual(6, stats.get("total"))
        self.assertAlmostEqual(2, stats.get("mean"))
        self.assertAlmostEqual(0.8164966, stats.get("stddev"))

    def testStandardDeviation(self):
        name = "test_stat"

        test_stat = Statistic(name, [2, 4, 4, 4, 5, 5, 7, 9], self.config)

        self.assertEqual(name, test_stat._name)

        stats = test_stat.stats()

        self.assertAlmostEqual(2, stats.get("stddev"))
