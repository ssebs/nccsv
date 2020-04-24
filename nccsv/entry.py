# entry.py - Text box with a border
import curses
from curses.textpad import Textbox, rectangle


class Entry():
    def __init__(self, stdscr, y, x, sizey, sizex, callback_on_enter):
        # Create window w/ border
        editwin = curses.newwin(sizey, sizex, y, x)
        rectangle(stdscr, 1-y, 1-x, sizey+y, sizex + x)

        # Render window
        stdscr.refresh()
        box = Textbox(editwin)
        box.edit(
            self.validate_enter_for_textbox
        )
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
