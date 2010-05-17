# Copyright (C) 2010 Peter Teichman

from ConfigParser import SafeConfigParser
import logging
import os
import sys
import time

from .stats import Accumulator, Statistic

log = logging.getLogger("instatrace")

class ExtractCommand:
    @classmethod
    def add_subparser(cls, parser):
        subparser = parser.add_parser("extract", help="Extract instatrace data from program log files")
        subparser.add_argument("--filter", action="store_true",
                               help="Filter out any lines that don't contain INSTATRACE")
        subparser.add_argument("file", nargs="+")
        subparser.set_defaults(run=cls.run,
                               filter_marker="INSTATRACE: ")

    @classmethod
    def run(cls, args):
        stats = Accumulator()

        marker = None
        if args.filter:
            marker = args.filter_marker

        for filename in args.file:
            stats.load(filename, None, marker)

        stats.dump(sys.stdout)

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
        stats = Accumulator()

        marker = None
        if args.filter:
            marker = args.filter_marker

        for filename in args.file:
            stats.load(filename, args.show_stats, marker)

        # load statistic configuration if requested
        config = SafeConfigParser({"layout": "exponential",
                                   "scale": "1"})
        if args.config is not None:
            config.read(args.config)

        names = stats.statistics.keys()
        names.sort()

        for i, name in enumerate(names):
            samples = stats.statistics.get(name)

            stat = Statistic(name, samples, config)
            stat.write_text_histogram(sys.stdout)

            if i != len(names)-1:
                sys.stdout.write("\n")
