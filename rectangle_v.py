"""
Module that implements the logic to find a proper rectangle vertically
"""

import json
import logging
from copy import deepcopy

from utils import Utils

# Setting logger
log = logging.getLogger(__name__)
fmt = logging.Formatter(datefmt="%H:%M:%S",
                        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
log.addHandler(sh)


class RectangleV():
    """
    Class  that implements the logic to find a proper rectangle vertically
    """

    def __init__(self, logLevel=logging.DEBUG):
        log.setLevel(logLevel)
        self.skyLineIn = None
        self.rect = None
        log.info("%s(%d) logLevel=%d", self.__class__.__name__, id(self), logLevel)

    def _calculate_area(self, r=None):
        if r != None and len(r) > 0:
            area = r['height'] * r['width']
            log.debug("_calculate_area r=%s area=%d",
                      str(r), area)
            return area
        return None

    def _has_positive_area(self,r=None):
        if r != None:
            positive_area = self._calculate_area(r) > 0
            log.debug("_has_positive_area r=%s %r",
                      str(r), positive_area)
            return positive_area
        return False

    def _is_vertical_rect(self, r=None):
        if r != None:
            is_vertical = r['height'] >= r['width'] and r['height'] > 0
            log.debug("_is_vertical_rect r=%s %r", str(r), is_vertical)
            return is_vertical
        return None

    def calculate_next_v_rect(self, skyLineIn=None):
        if skyLineIn != None:
            self.skyLineIn = skyLineIn
            if self.skyLineIn != None and len(self.skyLineIn) > 0:
                for r in self.skyLineIn:
                    if self._has_positive_area(r) and self._is_vertical_rect(r):
                        log.debug("calculate_next_v_rect rect=%s", str(r))
                        return deepcopy(r)
        return None

def run_rectangle_v():
    u = Utils()
    r = RectangleV()
    r.calculate_next_v_rect(
        json.loads(u.get_json_example_input())['sourceRectangles'])

if __name__ == '__main__':
    run_rectangle_v()