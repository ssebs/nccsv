# __init__.py

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


def render_filename_editor(stdscr):
    stdscr.clear()
    stdscr.addstr("Enter a filename (Hit ENTER to submit)")

    e = Entry(stdscr, 2, 0, 1, 15)
    e.edit_entry()
    return e.get_text()
# render_filename_editor


def render_editor(stdscr, filename, contents=None):
    stdscr.clear()
    h = 1
    w = 10
    x_pos = 0
    y_pos = 0
    if contents is None:
        contents = []
        # Create 2d array
        for i in range(5):
            contents.append([])
            for j in range(5):
                contents[i].append([])
        # Fill array
        for x in range(5):
            for y in range(5):
                contents[x][y] = Entry(
                    stdscr, 1+(y*3), 2+(x*(w+(w//2))+2), h, w)
    stdscr.refresh()

    while True:
        stdscr.clear()
        for x in range(len(contents)):
            for y in range(len(contents[0])):
                contents[x][y].render()

        # stdscr.refresh()

        contents[x_pos][y_pos].highlight()
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_DOWN and y_pos < len(contents[0])-1:
            contents[x_pos][y_pos].highlight()
            y_pos += 1
        elif key == curses.KEY_UP and y_pos > 0:
            contents[x_pos][y_pos].highlight()
            y_pos -= 1
        elif key == curses.KEY_RIGHT and x_pos < len(contents)-1:
            contents[x_pos][y_pos].highlight()
            x_pos += 1
        elif key == curses.KEY_LEFT and x_pos > 0:
            contents[x_pos][y_pos].highlight()
            x_pos -= 1
        elif key == ord("q"):
            break
        elif key == curses.KEY_ENTER or key in [10, 13]:
            contents[x_pos][y_pos].edit_entry()
            txt = contents[x_pos][y_pos].get_text()
            # stdscr.clear()
            # stdscr.addstr(0, 0, f"Entered: {txt}")
            # stdscr.refresh()
            # stdscr.getch()
        elif key == curses.KEY_DC or key == curses.KEY_DL:
            contents[x_pos][y_pos].clear_text()

        stdscr.refresh()

# render_editor


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
                stdscr.addstr(0, 0, "Creating {}".format(filename))
                stdscr.refresh()
                time.sleep(0.5)
                render_editor(stdscr, filename)
                break
            elif "Open" in menu[current_row]:
                filename = render_filename_editor(stdscr)
                stdscr.clear()
                stdscr.addstr(0, 0, "Opening {}".format(filename))
                stdscr.refresh()
                time.sleep(0.5)
                render_editor(stdscr, filename)
                break
            elif "Exit" in menu[current_row]:
                break

            stdscr.getch()

        render_menu(stdscr, current_row, menu)
        stdscr.refresh()
# main


if __name__ == "__main__":
    curses.wrapper(main)
