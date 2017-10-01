"""
Module that provides utilities for the application
"""

import os
import sys
import logging

# Setting logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

fmt = logging.Formatter(datefmt="%H:%M:%S",
                        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
log.addHandler(sh)

class Utils():
    """
    Class that implements the utilities for the application
    """

    def __init__(self, logLevel=logging.DEBUG):
        log.setLevel(logLevel)
        if dir(sys).__contains__('frozen'): # Mac bundle
            self.json_example_file = "example_input.json"
        else:
            self.abs_p = os.path.abspath(os.path.join(__file__, os.pardir))
            self.json_example_file = os.path.join(self.abs_p, "example_input.json")
        log.debug("json_example_file=%s", self.json_example_file)
        log.info("%s(%d) logLevel=%d", self.__class__.__name__, id(self), logLevel)

    def __read_file(self, fname=None):
        output = ""
        if not fname is None:
            with open(fname, 'r') as f:
                output = f.read()
        return output

    def get_json_example_input(self):
        log.debug("get_json_example_input file=%s",self.json_example_file)
        return self.__read_file(self.json_example_file)


def run_utils():
    u = Utils(logLevel=logging.DEBUG)
    u.get_json_example_input()


if __name__ == '__main__':
    run_utils()