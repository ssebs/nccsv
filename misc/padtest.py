# misc/padtest.py - te
import curses
from curses.textpad import Textbox, rectangle


def main_old(stdscr):
    h, w = stdscr.getmaxyx()
    stdscr.addstr(0, 0, "Pad should be below:")
    stdscr.addstr(
        h-1, 0, "wasd or arrow keys to scroll, q to quit",
        curses.A_REVERSE)

    stdscr.refresh()

    pad = curses.newpad(100, 100)
    pad_pos_y = 0
    pad_pos_x = 0

    # These loops fill the pad with letters
    for y in range(99):
        for x in range(99):
            pad.addch(y, x, ord('a') + (x*x+y*y) % 26)

    # pad position y, x; win pos y, x; win h, w
    #         ppy ppx wy wx  wh  ww
    pad.refresh(0, 0, 1, 0, h-2, w-1)
    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == ord('s') or key == curses.KEY_DOWN:
            pad_pos_y += 1
        elif key == ord('w') or key == curses.KEY_UP:
            pad_pos_y -= 1
        elif key == ord('d') or key == curses.KEY_RIGHT:
            pad_pos_x += 1
        elif key == ord('a') or key == curses.KEY_LEFT:
            pad_pos_x -= 1
        pad.refresh(pad_pos_y, pad_pos_x, 1, 0, h-2, w-1)


def rect(win, uly, ulx, lry, lrx, reverse=False):
    """Draw a rectangle with corners at the provided upper-left
    and lower-right coordinates.
    """
    if reverse:
        win.vline(uly+1, ulx, curses.ACS_VLINE,
                  lry - uly - 1, curses.A_REVERSE)
        win.hline(uly, ulx+1, curses.ACS_HLINE,
                  lrx - ulx - 1, curses.A_REVERSE)
        win.hline(lry, ulx+1, curses.ACS_HLINE,
                  lrx - ulx - 1, curses.A_REVERSE)
        win.vline(uly+1, lrx, curses.ACS_VLINE,
                  lry - uly - 1, curses.A_REVERSE)
        win.addch(uly, ulx, curses.ACS_ULCORNER, curses.A_REVERSE)
        win.addch(uly, lrx, curses.ACS_URCORNER, curses.A_REVERSE)
        win.addch(lry, lrx, curses.ACS_LRCORNER, curses.A_REVERSE)
        win.addch(lry, ulx, curses.ACS_LLCORNER, curses.A_REVERSE)
    else:
        win.vline(uly+1, ulx, curses.ACS_VLINE, lry - uly - 1)
        win.hline(uly, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
        win.hline(lry, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
        win.vline(uly+1, lrx, curses.ACS_VLINE, lry - uly - 1)
        win.addch(uly, ulx, curses.ACS_ULCORNER)
        win.addch(uly, lrx, curses.ACS_URCORNER)
        win.addch(lry, lrx, curses.ACS_LRCORNER)
        win.addch(lry, ulx, curses.ACS_LLCORNER)
# rect


class MyTextBox():
    """
    MyTextBox is a basic text editor
    """

    def __init__(self, win, refresh_method):
        self.win = win
        self.refresh_method = refresh_method
        self.max_x = 0
        self.max_y = 0
        self.update_screen_size()
        self.lastcmd = None
        self.stripspaces = 1
        win.keypad(True)

    def update_screen_size(self):
        maxy, maxx = self.win.getmaxyx()
        self.max_y = maxy - 1
        self.max_x = maxx - 1
    # update_screen_size

    def end_of_line(self, y):
        self.update_screen_size()
        last = self.max_x
        while True:
            if curses.ascii.ascii(self.win.inch(y, last)) != curses.ascii.SP:
                last = min(self.max_x, last + 1)
                break
            elif last == 0:
                break
            else:
                last = last - 1
        return last
    # end_of_line

    def insert_char(self, char):
        self.update_screen_size()
        (y, x) = self.win.getyx()
        back = None
        while y < self.max_y or x < self.max_x:
            oldchar = self.win.inch()
            try:
                self.win.addch(char)
            except curses.error:
                pass
            if not curses.ascii.isprint(oldchar):
                break
            char = oldchar
            (y, x) = self.win.getyx()
            if back is None:
                back = y, x
        if back is not None:
            self.win.move(*back)
    # insert_char

    def handle_command(self, char):
        self.update_screen_size()
        (y, x) = self.win.getyx()
        self.lastcmd = char

        # normal text
        if curses.ascii.isprint(char):
            if y < self.max_y or x < self.max_x:
                self.insert_char(char)
        # left or backspace
        elif char in (curses.ascii.STX, curses.KEY_LEFT,
                      curses.ascii.BS, curses.KEY_BACKSPACE, '\b', 127):
            if x > 0:
                self.win.move(y, x-1)
            elif y == 0:
                pass
            elif self.stripspaces:
                self.win.move(y-1, self.end_of_line(y-1))
            else:
                self.win.move(y-1, self.max_x)

            # backspace
            if char in (curses.ascii.BS, curses.KEY_BACKSPACE, '\b', 127):
                self.win.delch()
        # right
        elif char in (curses.ascii.ACK, curses.KEY_RIGHT):
            if x < self.max_x:
                self.win.move(y, x+1)
            elif y == self.max_y:
                pass
            else:
                self.win.move(y+1, 0)
        # down
        elif char in (curses.ascii.SO, curses.KEY_DOWN):
            if y < self.max_y:
                self.win.move(y+1, x)
                if x > self.end_of_line(y+1):
                    self.win.move(y+1, self.end_of_line(y+1))
        # up
        elif char in (curses.ascii.DLE, curses.KEY_UP):
            if y > 0:
                self.win.move(y-1, x)
                if x > self.end_of_line(y-1):
                    self.win.move(y-1, self.end_of_line(y-1))
        # enter
        elif char == curses.KEY_ENTER or char in [10, 13]:
            return 0
        return 1
    # handle_command

    def get_text(self):
        result = ""
        self.update_screen_size()
        for y in range(self.max_y + 1):
            self.win.move(y, 0)
            stop = self.end_of_line(y)
            if stop == 0 and self.stripspaces:
                continue
            for x in range(self.max_x + 1):
                if self.stripspaces and x > stop:
                    break
                result = result + chr(curses.ascii.ascii(self.win.inch(y, x)))
            if self.max_y > 0:
                result = result + "\n"
        return result
    # get_text

    def edit_text(self):
        while True:
            char = self.win.getch()
            if not char:
                continue
            if not self.handle_command(char):
                break
            # self.win.refresh()
            self.refresh_method()
        return self.get_text()
    # edit_text

# MyTextBox


class Entry():
    """
    Entry is a basic text editing box widget
    """

    def __init__(self, stdscr, y, x, sizey, sizex,
                 refresh_method,
                 default_text=None, callback_on_enter=None):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.size_y = sizey
        self.size_x = sizex
        self.text = default_text
        self.callback_on_enter = callback_on_enter
        self.has_edited = False
        self.is_highlighed = False
        self.refresh_method = refresh_method

        # Create window w/ border
        # self.container_win = curses.newwin(sizey+2, sizex+2, y, x)
        self.container_win = self.stdscr.derwin(sizey+2, sizex+2, y, x)
        self.editwin = self.container_win.derwin(sizey, sizex, 1, 1)

        self.render2()

        self.box = MyTextBox(self.editwin, self.refresh_method)
    # init

    def render2(self):
        # test: y=1,x=1,h=1,w=10
        if self.is_highlighed:
            if self.text:
                self.editwin.addstr(0, 0, self.text, curses.A_REVERSE)
            else:
                # self.editwin.addstr(0, 0, "N/A", curses.A_REVERSE)
                pass
            # reverse all the sides + corners
            self.container_win.border(
                curses.ACS_VLINE | curses.A_REVERSE,
                curses.ACS_VLINE | curses.A_REVERSE,
                curses.ACS_HLINE | curses.A_REVERSE,
                curses.ACS_HLINE | curses.A_REVERSE,
                curses.ACS_ULCORNER | curses.A_REVERSE,
                curses.ACS_URCORNER | curses.A_REVERSE,
                curses.ACS_LLCORNER | curses.A_REVERSE,
                curses.ACS_LRCORNER | curses.A_REVERSE,
            )
        else:
            if self.text:
                self.editwin.addstr(0, 0, self.text)
            else:
                # self.editwin.addstr(0, 0, "N/A", curses.A_REVERSE)
                pass
            # reverse all the sides + corners
            self.container_win.box()
        self.refresh_method()
    # render2

    def edit_entry(self):
        curses.curs_set(1)
        self.box.edit_text()
        curses.curs_set(0)

        self.has_edited = True
        self.text = self.box.get_text()
        self.is_highlighed = False

        return self.box.get_text()
    # edit_entry

    def get_text(self):
        if self.has_edited:
            return self.text
        else:
            return None
    # get_text

    def clear_text(self):
        self.text = None
        self.has_edited = False
        # need to also clear the text box, and set the cursor
        # self.box = None
        del self.box
        self.box = MyTextBox(self.editwin)
        self.highlight()
    # clear_text

    def highlight(self):
        self.is_highlighed = not self.is_highlighed
        self.render2()

    def validate_enter_for_textbox(self, x):
        if x == 10:
            return 7
        return x
    # validate_enter_for_textbox

    def __repr__(self):
        return self.text if self.text else ""
    # repr

# Entry


def main(stdscr):
    h, w = stdscr.getmaxyx()
    stdscr.addstr(0, 0, "Pad should be below:")
    stdscr.addstr(
        h-1, 0, "wasd or arrow keys to scroll, q to quit",
        curses.A_REVERSE)

    stdscr.refresh()

    pad = curses.newpad(100, 100)
    pad_pos_y = 0
    pad_pos_x = 0

    def do_refresh():
        pad.refresh(pad_pos_y, pad_pos_x, 1, 0, h-2, w-1)

    entr = Entry(pad, 1, 1, 1, 10, do_refresh)

    # do_refresh()
    pad.refresh(0, 0, 1, 0, h-2, w-1)
    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == ord('s') or key == curses.KEY_DOWN:
            pad_pos_y += 1
        elif key == ord('w') or key == curses.KEY_UP:
            pad_pos_y -= 1
        elif key == ord('d') or key == curses.KEY_RIGHT:
            pad_pos_x += 1
        elif key == ord('a') or key == curses.KEY_LEFT:
            pad_pos_x -= 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            entr.edit_entry()
        pad.refresh(pad_pos_y, pad_pos_x, 1, 0, h-2, w-1)


if __name__ == "__main__":
    curses.wrapper(main)
