# misc/padtest.py - te
import curses


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


if __name__ == "__main__":
    curses.wrapper(main)
