# derwin.py - testing a window within a window
import curses


def main(stdscr):
    # Create container window from stdscr
    sh, sw = stdscr.getmaxyx()
    container_win = curses.newwin(sh-1, sw-1, 1, 1)

    # Create inner window from container win
    bh, bw = container_win.getmaxyx()
    box_win = container_win.derwin(bh-2, bw-2, 1, 1)

    # Add size of inner win
    box_win.addstr(1, 1, f"{bh}x{bw}")

    # Draw borders
    container_win.box()
    box_win.box()

    # Render and wait for char
    container_win.refresh()
    container_win.getch()

# main


if __name__ == "__main__":
    curses.wrapper(main)
