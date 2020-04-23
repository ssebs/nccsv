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
    stdscr.addstr("Enter a filename (Hit CTRL + G to send)")

    editwin = curses.newwin(5, 30, 2, 1)
    rectangle(stdscr, 1, 0, 1+5+1, 1+30+1)
    stdscr.refresh()

    box = Textbox(editwin)
    box.edit(validate_enter_for_textbox)

    return box.gather()

# render_filename_editor


def render_editor(stdscr, filename, contents=None):
    stdscr.clear()

    if contents is None:
        contents = [[None for i in range(5)]for j in range(5)]
    
    for i, col in enumerate(contents):
        for j, x in enumerate(contents[i]):
            x = curses.newwin(1,30,j,1)
            rectangle(stdscr, 1, 0, 1+j+1, 1+30+1)
            stdscr.refresh()
            box = Textbox(x)
            box.edit(validate_enter_for_textbox)

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
            stdscr.addstr(0, 0, "You pressed {}".format(menu[current_row]))
            stdscr.refresh()

            if "New" in menu[current_row]:
                filename = render_filename_editor(stdscr)
                stdscr.clear()
                stdscr.addstr(0, 0, "Opening {}".format(filename))
                stdscr.refresh()
                render_editor(stdscr, filename)

            stdscr.getch()

        render_menu(stdscr, current_row, menu)
        stdscr.refresh()
# main


if __name__ == "__main__":
    curses.wrapper(main)
