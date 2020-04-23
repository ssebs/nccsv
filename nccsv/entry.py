# entry.py - Text box with a border
import curses
from curses.textpad import Textbox, rectangle


class Entry():
    def __init__(self, stdscr, y, x, sizey, sizex, callback_on_enter):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.callback_on_enter = callback_on_enter

        editwin = curses.newwin(sizey, sizex, 2, 1)
        rectangle(self.stdscr, 1, 0, 1+sizey+1, 1+sizex+1)
        self.stdscr.refresh()

        box = Textbox(editwin)
        box.edit(self.validate_enter_for_textbox)
        self.stdscr.refresh()
        callback_on_enter(stdscr, box.gather())
    # init

    def validate_enter_for_textbox(self, x):
        if x == 10:
            return 7
        return x
    # validate_enter_for_textbox

# Entry


if __name__ == "__main__":

    def callback_test(stdscr, txt):
        stdscr.clear()
        stdscr.addstr(0, 0, txt)
        stdscr.getch()

    def main(stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "Test")
        stdscr.getch()

        stdscr.clear()
        e = Entry(stdscr, 0, 0, 2, 6, callback_test)

    # main
    curses.wrapper(main)
