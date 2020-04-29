# grid.py - render multiple entries in a pad
import curses
# from nccsv.entry import Entry
from entry import Entry


class Grid():
    def __init__(self, size_y, size_x, h, w, win_pos_y, win_pos_x,
                 y_offset, x_offset, e_size_y, e_size_x):
        self.size_y = size_y
        self.size_x = size_x
        self.w = w
        self.h = h
        self.win_pos_y = win_pos_y
        self.win_pos_x = win_pos_x
        self.y_offset = y_offset
        self.x_offset = x_offset
        self.e_size_y = e_size_y
        self.e_size_x = e_size_x

        # Create 2D array for grid
        self.contents = []
        for i in range(self.size_x):
            self.contents.append([])
            for j in range(self.size_y):
                self.contents[i].append([])

        self.pos_y = 0
        self.pos_x = 0

        self.pad = curses.newpad(self.size_y, self.size_x)
        self.fill_grid()
    # init

    def fill_grid(self):
        tmp_win = curses.newwin(self.h-1, self.w-1, 0, 0)
        self.contents[0][0] = Entry(tmp_win, 0, 0, 4, 10)
        tmp_win.refresh()
        # for y in range(self.size_y-1):
        #     for x in range(self.size_x-1):
        #         self.contents[x][y] = Entry(self.pad,
        #                                     1+y, 2 + (x*self.e_size_x),
        #                                     # (x*(self.w+(self.w//2))+2),
        #                                     1, 10, render_ops={
        #                                         "py": self.pos_y,
        #                                         "px": self.pos_x,
        #                                         "h": self.h,
        #                                         "w": self.w,
        #                                         "wpy": self.win_pos_y,
        #                                         "wpx": self.win_pos_x,
        #                                         "esy": self.e_size_y,
        #                                         "esx": self.e_size_x
        #                                     })
    # fill_grid

    def render(self):
        self.pad.refresh(self.pos_y, self.pos_x,
                         self.win_pos_y, self.win_pos_x,
                         self.h - self.y_offset-1, self.w - self.x_offset-1)
    # render

    def add_row(self):
        pass
    # add_row

    def add_col(self):
        pass
    # add_col

    def handle_input(self, key=None):
        if not key:
            key = self.pad.getch()
        # TODO: check for min/max
        if key == ord('s') or key == curses.KEY_DOWN:
            self.pos_y += 1
        elif key == ord('w') or key == curses.KEY_UP:
            self.pos_y -= 1
        elif key == ord('d') or key == curses.KEY_RIGHT:
            self.pos_x += 1
        elif key == ord('a') or key == curses.KEY_LEFT:
            self.pos_x -= 1
        elif key == ord('q'):
            raise Exception("App closed")
        # self.render()
    # handle_input

# Grid


if __name__ == "__main__":
    def main(stdscr):
        h, w = stdscr.getmaxyx()
        stdscr.addstr(0, 0, "Grid test")
        stdscr.refresh()

        g = Grid(100, 100, h, w, 1, 0, 0, 0, 1, 10)
        g.render()
        while True:
            # ch = stdscr.getch()
            # if ch == ord('q'):
            #     break
            g.handle_input()
            g.render()

    # main
    curses.wrapper(main)
