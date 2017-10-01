"""
Module that implements the test utilites to verify the application
"""

import json
import logging
from copy import deepcopy
from random import randrange


# Setting logger
log = logging.getLogger(__name__)
fmt = logging.Formatter(datefmt="%H:%M:%S",
                        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
log.addHandler(sh)


class Test():
    """
    Class that implements the test utilites to verify the application
    """

    def __init__(self, logLevel=logging.DEBUG):
        log.setLevel(logLevel)
        self.percentageRect = 0.7
        self.percentageCoords = 0.5
        log.info("%s(%d) logLevel=%d", self.__class__.__name__, id(self), logLevel)

    def _generate_test_example(self, numRectsMax=None, widthMax=None, heightMax=None):
        if numRectsMax != None and heightMax != None and widthMax != None:
            log.debug("_generate_test_example numRectsMax=%d heightMax=%d widthMax=%d percentageRect=%f percentageCoords=%f",
                      numRectsMax, heightMax, widthMax, self.percentageRect, self.percentageCoords)
            rects = []
            numRectsMin = int(numRectsMax*self.percentageRect)
            heightMin = int(heightMax*self.percentageCoords)
            widthMin = int(widthMax*self.percentageCoords)
            numRects = randrange(numRectsMin, numRectsMax)
            x = 0
            y = heightMax
            for i in range(numRects):
                rect = self._generate_rect_coords(x,y,widthMin,widthMax,heightMin,heightMax)
                if rect == None:
                    break
                x += rect['width']
                rects.append(rect)
            skyline = {}
            skyline['numRects'] =deepcopy(numRects)
            skyline['sourceRectangles'] = deepcopy(rects)
            return skyline
        return None

    def _generate_rect_coords(self, x=None, y=None, widthMin=None, widthMax=None, heightMin=None, heightMax=None):
        if x != None and x >= 0 and y != None and y >= 0 \
                and widthMin != None and widthMax != None \
                and heightMin != None and heightMax != None :
            log.debug("_generate_rect_coords x=%d y=%d widthMin=%d widthMax=%d heightMin=%d heightMax=%d",
                      x, y, widthMin, widthMax, heightMax, heightMax)
            rect = {}
            rect['x'] = x
            rect['y'] = y
            rect['width'] = randrange(widthMin, widthMax)
            rect['height'] = randrange(heightMin, heightMax)
            return rect
        return None

    def generate_test_example(self):
        skyline = self._generate_test_example(8, 50, 145)
        log.debug("generate_test_example skyline=%s", str(skyline))
        return json.dumps(skyline)

def run_test():
    t = Test()
    t.generate_test_example()

if __name__ == '__main__':
    run_test()