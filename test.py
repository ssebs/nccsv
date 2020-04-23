import curses
from curses.textpad import rectangle, Textbox


def validator(x):
    """ Make enter submit """
    if x == 10:
        return 7
    return x
# validator


def main(stdscr):
    # Don't show the cursor
    curses.curs_set(0)

    # "Print"
    stdscr.addstr(0, 0, "Test!")
    # Load the changes we made
    stdscr.refresh()

    # wait for user input (don't exit the app)
    stdscr.getch()
    # Clear the screen
    stdscr.clear()

    win1 = curses.newwin(5, 10, 0, 0)
    rectangle(stdscr, 0, 0, 5, 10)
    stdscr.refresh()

    # wait for user input (don't exit the app)
    stdscr.getch()
    stdscr.clear()

    stdscr.addstr(0, 0, "What's your name?")
    # height, width, where to place y, where to place x
    #                    h, w, y, x
    win2 = curses.newwin(2, 10, 2, 1)
    #  a,b--
    #  |   |
    #  --c,d
    #          screen, b,a,d,c
    rectangle(stdscr, 1, 0, 5, 11)
    stdscr.refresh()

    text_edit = Textbox(win2)
    text_edit.edit(validator)

    stdscr.refresh()
    stdscr.clear()

    txt = text_edit.gather()
    txt = txt.strip()

    stdscr.addstr(0, 0, f"Hi, {txt}!")

    stdscr.getch()
# main


if __name__ == "__main__":
    curses.wrapper(main)
