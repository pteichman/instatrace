# Copyright (C) 2010 Peter Teichman

import logging
import os
import sys
import time

from .stats import Histogram, Statistics

log = logging.getLogger("instatrace")

class HistogramsCommand:
    @classmethod
    def add_subparser(cls, parser):
        subparser = parser.add_parser("histograms", help="Stat histograms")
        subparser.add_argument("file", nargs="+")
        subparser.set_defaults(run=cls.run)

    @staticmethod
    def run(args):
        stats = Statistics()

        for filename in args.file:
            count = 0
            fd = open(filename)
            for line in fd.xreadlines():
                line = line.strip()

                stat = line.split(" ", 2)
                stats.add_sample(stat[0], int(stat[1]))

            fd.close()

        names = stats.statistics.keys()
        names.sort()

        for name in names:
            histogram = stats.statistics.get(name)
            histogram.text(sys.stdout)
