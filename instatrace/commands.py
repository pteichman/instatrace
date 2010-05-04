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
        subparser.add_argument("--filter", action="store_true",
                               help="Filter out any lines that don't contain INSTATRACE")
        subparser.add_argument("file", nargs="+")
        subparser.set_defaults(run=cls.run,
                               filter_marker="INSTATRACE: ")

    @staticmethod
    def run(args):
        stats = Statistics()

        for filename in args.file:
            count = 0
            fd = open(filename)
            for line in fd.xreadlines():
                if args.filter:
                    pos = line.find(args.filter_marker)
                    if pos == -1:
                        continue
                    line = line[pos+len(args.filter_marker):]

                line = line.strip()

                stat = line.split(" ", 2)
                stats.add_sample(stat[0], int(stat[1]))

            fd.close()

        names = stats.statistics.keys()
        names.sort()

        for name in names:
            histogram = stats.statistics.get(name)
            histogram.text(sys.stdout)
