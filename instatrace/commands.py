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
        subparser.add_argument("-c", "--config",
                               help="Statistics configuration file")
        subparser.add_argument("--filter", action="store_true",
                               help="Filter out any lines that don't contain INSTATRACE")
        subparser.add_argument("-s", "--stat", action="append",
                               dest="show_stats", metavar="STAT",
                               help="Ignore stats not matching STAT")
        subparser.add_argument("file", nargs="+")
        subparser.set_defaults(run=cls.run,
                               filter_marker="INSTATRACE: ")

    @classmethod
    def run(cls, args):
        stats = Statistics(configfile=args.config)

        for filename in args.file:
            marker = None
            if args.filter:
                marker = args.filter_marker

            stats.load(filename, args.show_stats, marker)

        names = stats.statistics.keys()
        names.sort()

        for i, name in enumerate(names):
            histogram = stats.statistics.get(name)
            histogram.text(sys.stdout)

            if i != len(names)-1:
                sys.stdout.write("\n")
