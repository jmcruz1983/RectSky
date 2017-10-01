"""
Module that implements the logic to find a proper rectangle horizontally
"""

import json
import logging
from utils import Utils

# Setting logger
log = logging.getLogger(__name__)
fmt = logging.Formatter(datefmt="%H:%M:%S",
                        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
log.addHandler(sh)


class RectangleH():
    """
    Class  that implements the logic to find a proper rectangle horizontally
    """

    def __init__(self, logLevel=logging.DEBUG):
        log.setLevel(logLevel)
        self.skyLineIn = None
        self.rect = None
        log.info("%s(%d) logLevel=%d", self.__class__.__name__, id(self), logLevel)

    def calculate_area(self, r=None):
        if r != None and len(r) > 0:
            area = r['height'] * r['width']
            log.debug("calculate_area r=%s area=%d",
                      str(r), area)
            return area
        return None

    def has_positive_area(self,r=None):
        if r != None:
            positive_area = self.calculate_area(r) > 0
            log.debug("has_positive_area r=%s %r",
                      str(r), positive_area)
            return positive_area
        return False

    def _get_rect_y_by_x(self, x=None):
        if x != None and self.skyLineIn != None and len(self.skyLineIn) > 0:
            for r in self.skyLineIn:
                if r['x'] == x:
                    log.debug("_get_rect_y_by_x x=%d y=%d", x, r['y'])
                    return r['y']
        return None

    def contains_x_y(self, r=None, x=None, y=None):
        if r != None and x != None and y != None:
            contains_x_y = (r['x'] <= x or x <= r['x']+r['width']) and (r['y'] <= y or y <= r['y']-r['height'])
            log.debug("contains_x_y rect=%s x=%d y=%d %r", str(r), x, y, contains_x_y)
            return contains_x_y
        return False

    def _calculate_x_y(self):
        if self.skyLineIn != None and len(self.skyLineIn) > 0:
            idx = 0
            for r in self.skyLineIn:
                if self.has_positive_area(r):
                    idx =  self.skyLineIn.index(r)
                    break
            x = self.skyLineIn[idx]['x']
            y = self.skyLineIn[idx]['y']
            log.debug("_calculate_x_y idx=%d x=%d y=%d", idx, x, y)
            return x,y
        return None

    def _get_next_rect(self, r):
        if r != None:
            idx = self.skyLineIn.index(r)
            if len(self.skyLineIn) > idx +1:
                next_r = self.skyLineIn[idx+1]
                log.debug("_get_next_rect r=%s idx=%s next_r=%s", str(r), idx+1, next_r)
                return next_r
        return None

    def _is_adjacent(self,r1=None,r2=None):
        if r1 != None and r2 != None:
            is_adj = (r1['x']+r1['width'])==r2['x']
            log.debug("_is_adjacent r1=%s r2=%s %r",
                      str(r1), str(r2), is_adj)
            return is_adj
        return False

    def _loop_to_next_rect(self, r=None):
        next_r = self._get_next_rect(r)
        if next_r != None:
            loop_to_next = self._is_adjacent(r, next_r) and self.has_positive_area(r)
        else: #last rect
            loop_to_next = self.has_positive_area(r)
        log.debug("_loop_to_next_rect %s %r ", str(r), loop_to_next)
        return loop_to_next

    def _is_horizontal_rect(self, r=None):
        if r != None:
            is_horizontal = r['width'] > r['height'] and r['width'] > 0
            log.debug("_is_horizontal_rect r=%s %r", str(r), is_horizontal)
            return is_horizontal
        return None

    def _get_first_valid_h(self):
        if self.skyLineIn != None and len(self.skyLineIn) > 0:
            for r in self.skyLineIn:
                if self.has_positive_area(r):
                    log.debug("_get_first_valid_h h=%d ", r['height'])
                    return r['height']
        return None

    def _get_max_valid_h(self):
        if self.skyLineIn != None and len(self.skyLineIn) > 0:
            max_h = self._get_first_valid_h()
            if max_h != None:
                for r in self.skyLineIn:
                    if self.has_positive_area(r):
                        if max_h < r['height']:
                            max_h = r['height']
                log.debug("_get_max_valid_h h=%d ", max_h)
                return max_h
        return None

    def _find_rect_idx_x_y(self, x=None, y=None):
        if self.skyLineIn != None and len(self.skyLineIn) > 0 and x != None and y != None:
            idx = 0
            for r in self.skyLineIn:
                if x == r['x'] and y == r['y']:
                    idx = self.skyLineIn.index(r)
                    log.debug("_find_rect_idx_x_y x=%d y=%d idx=%d", x, y, idx)
                    return idx
        return None

    def _calculate_w_h(self, x,y):
        if self.skyLineIn != None and len(self.skyLineIn) > 0:
            w = 0
            idx = self._find_rect_idx_x_y(x,y)
            if idx != None and len(self.skyLineIn) > idx:
                h = self._get_max_valid_h()
                if h != None:
                    for r in self.skyLineIn[idx:]:
                        if self._loop_to_next_rect(r) != True:
                            break
                        w += r['width']
                        if r['height'] < h:
                            h = r['height']
                    log.debug("_calculate_w_h w=%d h=%d ", w, h)
                    return w,h
        return None

    def _calculate_next_h_rect(self):
        rect = {}
        xy = self._calculate_x_y()
        if xy != None:
            x,y = xy
            wh = self._calculate_w_h(x,y)
            if wh != None:
                w,h = wh
                rect['x'] = x
                rect['y'] = y
                rect['width'] = w
                rect['height'] = h
                log.debug("_calculate_next_h_rect rect=%s", str(rect))
                return rect
        return None

    def calculate_next_h_rect(self, skyLineIn=None):
        if skyLineIn != None:
            self.skyLineIn = skyLineIn
            rect = self._calculate_next_h_rect()
            if self._is_horizontal_rect(rect):
                log.info("calculate_next_h_rect rect=%s", str(rect))
                return rect
        return None


def run_rectangle_h():
    u = Utils()
    r = RectangleH()
    r.calculate_next_h_rect(
        json.loads(u.get_json_example_input())['sourceRectangles'])

if __name__ == '__main__':
    run_rectangle_h()