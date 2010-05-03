# Copyright (C) 2010 Peter Teichman

import argparse
import logging
import sys

from . import commands

parser = argparse.ArgumentParser(description="Instastat control")
parser.add_argument("-s", "--stats", default="insta.stats")
parser.add_argument("--debug", action="store_true", help=argparse.SUPPRESS)

subparsers = parser.add_subparsers(title="Commands")
commands.HistogramsCommand.add_subparser(subparsers)

def main():
    args = parser.parse_args()

    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logging.root.addHandler(console)

    if args.debug:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)

    try:
        args.run(args)
    except KeyboardInterrupt:
        print
        sys.exit(1)

if __name__ == "__main__":
    main()
