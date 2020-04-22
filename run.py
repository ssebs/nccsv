import curses
import time


def render_menu(stdscr, selected_row, menu):
    h, w = stdscr.getmaxyx()

    for i, text in enumerate(menu):
        x = w//2 - len(text)//2
        y = h//2 - len(menu)//2 + i
        if selected_row == i:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, text)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, text)

    stdscr.refresh()

# render_menu


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    menu = ["New CSV File", "Open CSV File", "Exit"]
    current_row = 0

    # render first time
    render_menu(stdscr, current_row, menu)
    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu):
            current_row += 1
        elif key == ord("q"):
            break
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            stdscr.addstr(0, 0, "You pressed {}".format(menu[current_row]))
            stdscr.refresh()
            stdscr.getch()

        render_menu(stdscr, current_row, menu)
        stdscr.refresh()
# main


if __name__ == "__main__":
    curses.wrapper(main)
