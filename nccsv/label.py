# entry.py - Text display with a border
import curses


class Label():
    """
    Label is a basic text widget
    """

    def __init__(self, stdscr, y, x, sizey, sizex,
                 default_text="None", has_border=False):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.size_y = sizey
        self.size_x = sizex
        self.text = default_text
        self.has_border = has_border

        # Create window w/ border
        self.container_win = self.stdscr.derwin(sizey+2, sizex+2, y, x)
        self.editwin = self.container_win.derwin(sizey, sizex, 1, 1)

        self.render2()

        # self.container_win.addstr(0, 0, "test")
        self.editwin.addstr(0, 0, self.text)
    # init

    def render2(self):
        if self.has_border:
            self.container_win.box()

    # render2

# Label
