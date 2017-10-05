"""
Module that implements the GUI for the application
"""


import json
import logging
from Tkinter import *
from copy import deepcopy

from test import Test
from utils import Utils
from skyline import SkyLine

# Setting logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

fmt = logging.Formatter(datefmt="%H:%M:%S",
                        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
log.addHandler(sh)

class Gui():
    """
    Class that implements the GUI for the application
    """

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('logLevel'):
            logLevel = kwargs['logLevel']
        else:
            logLevel = logging.INFO
        log.setLevel(logLevel)
        self._init_vars()
        self.utils = Utils(logLevel)
        self.skyline = SkyLine(logLevel)
        self.test = Test(logLevel)
        self._create_root_window()
        self._add_plot_canvas()
        self._add_text_input()
        self._add_clear_button()
        self._add_random_button()
        self._add_solve_button()
        self._add_copy_button()
        self._plot_example_source_rectangles()
        log.info("%s(%d) logLevel=%d", self.__class__.__name__, id(self), logLevel)

    def _init_vars(self):
        self._tag = None
        self._tag_result = None
        self._rect_dict = None
        self._base_offset_x = 10
        self._factor = 1.1

    def _create_root_window(self):
        self._root = Tk()
        self._root.title("RectSky")

    def _add_plot_canvas(self):
        self._plot_canvas = Canvas(self._root, borderwidth=0, bg="#EDEDED")
        self._plot_canvas.pack(side=LEFT)
        self._plot_canvas.bind("<Motion>", self._draw_coords)

        self._plot_canvas_result = Canvas(self._root, borderwidth=0, bg="#EDEDED")
        self._plot_canvas_result.pack(side=RIGHT)
        self._plot_canvas_result.bind("<Motion>", self._draw_coords_result)

    def _draw_coords(self, event, off_x=10, off_y=0):
        if not self._tag is None:
            self._plot_canvas.delete(self._tag)
        self._tag = self._plot_canvas\
            .create_text(event.x+off_x, event.y+off_y,
                         text="(%r, %r)" % (event.x-self._base_offset_x, event.y), anchor="nw")

    def _draw_coords_result(self, event, off_x=10, off_y=0):
        if not self._tag_result is None:
            self._plot_canvas_result.delete(self._tag_result)
        self._tag_result = self._plot_canvas_result\
            .create_text(event.x+off_x, event.y+off_y,
                         text="(%r, %r)" % (event.x-self._base_offset_x, event.y), anchor="nw")

    def _calculate_coords(self, x, y, w, h):
        x0 = x+self._base_offset_x
        x1 = x0+w
        return x0, y, x1, y-h

    def _plot_rectangle(self, r=None, w=1, outline="black", dash=None, source=True):
        if not r is None:
            x0, y0, x1, y1 = self._calculate_coords(r['x'], r['y'], r['width'], r['height'])
            if source:
                self._plot_canvas.create_rectangle(x0, y0, x1, y1,
                                                   width=w, outline=outline, dash=dash)
            else:
                self._plot_canvas_result.create_rectangle(x0, y0, x1, y1,
                                                   width=w, outline=outline, dash=dash)

    def _clear_canvas(self):
        self._plot_canvas.delete("all")
        self._plot_canvas_result.delete("all")

    def _add_text_input(self):
        self.txt_in = Text(self._root)
        self.txt_in.configure(width=90, height=10)
        self.txt_in.pack()
        self._rect_dict = self._parse_json(self.utils.get_json_example_input())
        self._update_text_input()

    def _get_text_input(self):
        return self.txt_in.get("1.0",'end-1c')

    def _parse_json(self, txt):
        try:
            return json.loads(txt)
        except ValueError, e:
            msg = "Wrong JSON!" if len(txt) > 0 else "Empty JSON!"
            self._popup(title="Error",
                        msg=msg)
            return None

    def _pretty_print(self, txt=None):
        if txt != None:
            return txt.encode("ascii")\
                .replace('"numRects"', '\n\t"numRects"')\
                .replace('"sourceRectangles"', '\n\t"sourceRectangles"')\
                .replace('"rectangles"', '\n\t"rectangles"')\
                .replace("},", "},\n\t\t")
        return ""

    def _clear_text_input(self):
        self.txt_in.delete("1.0", END)

    def _update_text_input(self, txt=None, pretty_print=True):
        if txt == None:
            txt = deepcopy(json.dumps(self._rect_dict))
        self._clear_text_input()
        if pretty_print:
            txt = self._pretty_print(txt)
        self.txt_in.insert("1.0", txt)

    def _add_clear_button(self):
        self.clear_bt = Button(self._root, text='Clear', command=self._clear_button_pressed)
        self.clear_bt.pack(side=LEFT)

    def _add_random_button(self):
        self.random_bt = Button(self._root, text='Random', command=self._random_button_pressed)
        self.random_bt.pack(side=LEFT)

    def _add_solve_button(self):
        self.solve_bt = Button(self._root, text='Solve', command=self._solve_button_pressed)
        self.solve_bt.pack(side=LEFT)

    def _add_copy_button(self):
        self.copy_bt = Button(self._root, text='Copy', command=self._copy_button_pressed)
        self.copy_bt.pack(side=RIGHT)

    def _popup(self, title=None, msg=None, w=200, h=50):
        if not title is None and not msg is None:
            p = Toplevel()
            p.title("Error")
            p.geometry('%dx%d'%(w,h))
            m = Message(p, text=msg)
            m.configure(width=w)
            m.pack()
            b = Button(p, text="Close", command=p.destroy)
            b.pack()

    def _clear_button_pressed(self):
        self._clear_text_input()
        self._clear_canvas()

    def _plot_source_rectangles(self, text_input=None):
        self._rect_dict = deepcopy(self._parse_json(text_input))
        if self._rect_dict != None and 'sourceRectangles' in self._rect_dict:
            log.debug("_plot_source_rectangles")
            self._clear_canvas()
            for r in self._rect_dict['sourceRectangles']:
                self._plot_rectangle(r, w=1, outline="blue")

    def _plot_result_rectangles(self):
        if self._rect_dict != None and 'sourceRectangles' in self._rect_dict:
            log.debug("_plot_result_rectangles")
            skyLineOut = self.skyline.get_rectangles(self._rect_dict['sourceRectangles'])
            if skyLineOut != None:
                self._rect_dict['rectangles'] = deepcopy(skyLineOut)
                self._update_text_input()
                for r in self._rect_dict['rectangles']:
                    self._plot_rectangle(r, w=1, outline="red", source=False)

    def _plot_example_source_rectangles(self):
        txt = self.utils.get_json_example_input()
        self._update_text_input(txt)
        self._plot_source_rectangles(txt)

    def _random_button_pressed(self):
        txt = self.test.generate_test_example()
        self._update_text_input(txt)
        self._plot_source_rectangles(txt)

    def _solve_button_pressed(self):
        txt = self._get_text_input()
        self._update_text_input(txt, pretty_print=False)
        self._plot_source_rectangles(txt)
        self._plot_result_rectangles()

    def _copy_button_pressed(self):
        self._root.clipboard_clear()
        self._root.clipboard_append(self._get_text_input())
        self._root.update()

    def run_gui(self):
        if self._root:
            self._root.mainloop()


def run_app(*args, **kwargs):
    g = Gui(*args, **kwargs)
    g.run_gui()


if __name__ == '__main__':
    run_app(logLevel=logging.DEBUG)