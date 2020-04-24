# entry.py - Text box with a border
import curses
from curses.textpad import Textbox, rectangle


class Entry():
    def __init__(self, stdscr, y, x, sizey, sizex, callback_on_enter=None):
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        self.stdscr = stdscr
        self.callback_on_enter = callback_on_enter
        self.has_edited = False
        self.text = None

        # Create window w/ border
        #                        h       w    y  x
        editwin = curses.newwin(sizey, sizex, y, x)
        #                     y    x     hy       wx
        rectangle(stdscr, abs(1-y), abs(1-x), sizey+y, sizex + x)

        # Render window
        stdscr.refresh()
        self.box = Textbox(editwin)

        if self.has_edited:
            self.text = self.box.gather()
    # init

    def edit_entry(self):
        curses.curs_set(1)
        self.box.edit(
            self.validate_enter_for_textbox
        )
        curses.curs_set(0)
        if self.callback_on_enter is not None:
            self.callback_on_enter(self.stdscr, self.text)

        self.has_edited = True
        self.text = self.box.gather()

        return self.box.gather()
    # edit_entry

    def get_text(self):
        if self.has_edited:
            return self.text
        else:
            return None
    # get_text

    def validate_enter_for_textbox(self, x):
        if x == 10:
            return 7
        return x
    # validate_enter_for_textbox

# Entry


if __name__ == "__main__":

    def callback_test(stdscr, txt):
        stdscr.clear()
        stdscr.addstr(0, 0, f"You typed: {txt}")

    def main(stdscr):
        curses.curs_set(0)

        # stdscr.addstr(0, 0, "Test")
        # stdscr.getch()

        stdscr.clear()
        e = Entry(stdscr, 1, 1, 1, 10, callback_test)

        # box = curses.newwin(20,20,5,5)
        # box.box()

        # stdscr.refresh()
        # box.refresh()

        stdscr.getch()
    # main
    curses.wrapper(main)
