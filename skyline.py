"""
Module that implements the logic to find the skyline based on horizontal rectangles
"""


import json
import logging
from pprint import pprint

from utils import Utils
from copy import deepcopy
from rectangle_h import RectangleH
from rectangle_v import RectangleV

# Setting logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

fmt = logging.Formatter(datefmt="%H:%M:%S",
                        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
log.addHandler(sh)

class SkyLine():
    """
    Class that implements the logic to find the skyline based on horizontal rectangles
    """

    def __init__(self, logLevel=logging.DEBUG):
        log.setLevel(logLevel)
        self.skyLineIn = None
        self.skyLineAux = None
        self.skyLineOut = []
        self.r_h = RectangleH()
        self.r_v = RectangleV()
        log.info("%s(%d) logLevel=%d", self.__class__.__name__, id(self), logLevel)

    def _calculate_area_skyline(self, skyLine=None):
        if skyLine != None:
            totalArea = 0
            for r in skyLine:
                totalArea += self.r_h.calculate_area(r)
                log.debug("_calculate_area_skyline %d", totalArea)
            return totalArea
        return None

    def _skyline_has_positive_area(self, skyLine=None):
        positive_area = self._calculate_area_skyline(skyLine) > 0
        log.debug("_skyline_has_positive_area %r", positive_area)
        return positive_area

    def _find_rect_idx_x_y(self, rect=None):
        if self.skyLineIn != None and len(self.skyLineIn) > 0 and rect != None:
            idx = 0
            for r in self.skyLineIn:
                if rect['x'] == r['x'] and rect['y'] == r['y']:
                    idx = self.skyLineIn.index(r)
                    log.debug("_find_rect_idx_x_y x=%d y=%d idx=%d", rect['x'], rect['y'], idx)
                    return idx
        return None

    def _subtract_h_rect(self, rect=None):
        updated = False
        if rect != None:
            idx = self._find_rect_idx_x_y(rect)
            if idx != None and len(self.skyLineIn) > idx:
                for r in self.skyLineIn[idx:]:
                    if self.r_h.contains_x_y(rect, r['x'], r['y']):
                        if self.r_h.has_positive_area(r) == False:
                            break
                        r['y'] = r['y'] - rect['height']
                        r['height'] = r['height'] - rect['height']
                        updated = True
        log.debug("_subtract_h_rect rect=%s %r", str(rect), updated)
        return updated

    def _subtract_v_rect(self, rect=None):
        updated = False
        if rect != None:
            for r in self.skyLineIn:
                if r == rect:
                    r['height'] = r['height'] - rect['height']
                    updated = True
                    break
        log.debug("_subtract_v_rect rect=%s %r", str(rect), updated)
        return updated

    def _remove_rects_with_no_area(self):
        skyLineInNew = []
        if self.skyLineIn != None and len(self.skyLineIn) > 0:
            for r in self.skyLineIn:
                if self.r_h.has_positive_area(r):
                    skyLineInNew.append(r)
        log.debug("_remove_rects_with_no_area skyLineInNew=%s", str(skyLineInNew))
        return skyLineInNew

    def _check_covered_area(self, r=None):
        if r != None:
            totalAreaBefore = self._calculate_area_skyline(self.skyLineAux)
            rectArea = self.r_h.calculate_area(r)
            totalAreaAfter = self._calculate_area_skyline(self.skyLineIn)
            covered_area = totalAreaBefore == totalAreaAfter + rectArea
            log.debug("_check_covered_area %r", covered_area)
            return covered_area
        return False

    def _build_skyline(self):
        count = 0
        while(self._skyline_has_positive_area(self.skyLineIn)):
            count+=1
            if count > 30:
                break
            log.debug("_build_skyline count=%d", count)
            rect_h = {}
            while(rect_h != None):
                rect_h = self.r_h.calculate_next_h_rect(self.skyLineIn)
                if rect_h != None:
                    self.skyLineAux = deepcopy(self.skyLineIn) # backup security
                    if(self._subtract_h_rect(rect_h) and self._check_covered_area(rect_h)):
                        self.skyLineOut.append(rect_h)
                    else:
                        self.skyLineIn = deepcopy(self.skyLineAux)
            rect_v = {}
            while(rect_v != None):
                rect_v = self.r_v.calculate_next_v_rect(self.skyLineIn)
                if rect_v != None:
                    self.skyLineAux = deepcopy(self.skyLineIn) # backup security
                    if(self._subtract_v_rect(rect_v) and self._check_covered_area(rect_v)):
                        self.skyLineOut.append(rect_v)
                    else:
                        self.skyLineIn = deepcopy(self.skyLineAux)

    def get_rectangles(self, skyLineIn):
        if skyLineIn != None :
            del self.skyLineIn
            del self.skyLineAux
            del self.skyLineOut
            self.skyLineIn = deepcopy(skyLineIn)
            self.skyLineAux = deepcopy(skyLineIn)
            self.skyLineOut = []
            self._build_skyline()
            return self.skyLineOut
        return None

def run_skyline():
    u = Utils()
    s = SkyLine()
    s.get_rectangles(json.loads(u.get_json_example_input())['sourceRectangles'])


if __name__ == '__main__':
    run_skyline()