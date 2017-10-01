#! /usr/bin/env python

import logging
import argparse
from gui import run_app

# Setting logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

fmt = logging.Formatter(datefmt="%H:%M:%S",
                        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
log.addHandler(sh)


def parse_cmds():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="Enables verbose logging")
    args = parser.parse_args()
    parser.print_help()
    if args.verbose:
        run_app(logLevel=logging.DEBUG)
    else:
        run_app(logLevel=logging.INFO)


if __name__ == '__main__':
    parse_cmds()