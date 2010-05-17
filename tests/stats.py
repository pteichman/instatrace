# Copyright (C) 2010 Peter Teichman

from ConfigParser import SafeConfigParser
import unittest

from instatrace.stats import Accumulator, Statistic

class testStatistics(unittest.TestCase):
    def setUp(self):
        self.config = SafeConfigParser({"layout": "exponential",
                                        "scale": "1"})

    def tearDown(self):
        self.config = None

    def testStats(self):
        name = "test_stat"
        s = Accumulator()

        s.add_sample(name, 1)
        s.add_sample(name, 2)
        s.add_sample(name, 3)

        samples = s.statistics.get(name)
        test_stat = Statistic(name, samples, self.config)

        self.assertEqual(name, test_stat._name)

        stats = test_stat.stats()

        self.assertEqual(3, stats.get("count"))
        self.assertEqual(6, stats.get("total"))
        self.assertAlmostEqual(2, stats.get("mean"))
        self.assertAlmostEqual(0.8164966, stats.get("stddev"))

    def testStandardDeviation(self):
        name = "test_stat"

        s = Accumulator()

        s.add_sample(name, 2)
        s.add_sample(name, 4)
        s.add_sample(name, 4)
        s.add_sample(name, 4)
        s.add_sample(name, 5)
        s.add_sample(name, 5)
        s.add_sample(name, 7)
        s.add_sample(name, 9)

        samples = s.statistics.get(name)
        test_stat = Statistic(name, samples, self.config)

        self.assertEqual(name, test_stat._name)

        stats = test_stat.stats()

        self.assertAlmostEqual(2, stats.get("stddev"))
