from nccsv.entry import Entry
import time
import curses
from curses.textpad import Textbox, rectangle


def render_menu(stdscr, selected_row, menu):
    h, w = stdscr.getmaxyx()

    for i, text in enumerate(menu):
        x = w//2 - len(text)//2
        y = h//2 - len(menu)//2 + i
        if selected_row == i:
            stdscr.addstr(y, x, text, curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, text)

    stdscr.refresh()

# render_menu


def validate_enter_for_textbox(x):
    if x == 10:
        return 7
    return x
# validate_enter_for_textbox


def render_filename_editor(stdscr):
    stdscr.clear()
    stdscr.addstr("Enter a filename (Hit ENTER to submit)")

    e = Entry(stdscr, 0, 0, 1, 15)
    return e.get_text()
# render_filename_editor


def render_editor(stdscr, filename, contents=None):
    stdscr.clear()

    position_x = 0
    position_y = 0

    if contents is None:
        contents = []
        for x in range(5):
            for y in range(5):
                contents.append(
                    curses.newwin(2, 10, y, x)
                )
                rectangle(stdscr, y*2, x*10, 2+(y*2), 10+(x*10))

    stdscr.refresh()

    key = stdscr.getch()
    if key == curses.KEY_DOWN:
        position_y += 1

    # Handle editing / positioning
    box = Textbox(
        contents[position_y]
    )
    box.edit(validate_enter_for_textbox)
    box.gather()
    stdscr.refresh()

# render_editor


def render_editor_2(stdscr, filename, contents=None):
    stdscr.clear()

    stdscr.refresh()

# render_editor_2


def main(stdscr):
    curses.curs_set(0)

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

            if "New" in menu[current_row]:
                filename = render_filename_editor(stdscr)
                stdscr.clear()
                stdscr.addstr(0, 0, "Opening {}".format(filename))
                stdscr.refresh()
                time.sleep(1)
                # render_editor(stdscr, filename)
            elif "Open" in menu[current_row]:
                filename = render_filename_editor(stdscr)
                stdscr.clear()
                stdscr.addstr(0, 0, "Opening {}".format(filename))
                stdscr.refresh()
                time.sleep(1)
                render_editor_2(stdscr, filename)
            elif "Exit" in menu[current_row]:
                break

            stdscr.getch()

        render_menu(stdscr, current_row, menu)
        stdscr.refresh()
# main


if __name__ == "__main__":
    curses.wrapper(main)
