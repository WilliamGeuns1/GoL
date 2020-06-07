import os
import sys
import time
import json
import random
import argparse
import curses
import numpy as np

class GameOfLife():
    def __init__(self, height, width, randomize, pattern):
        self.listen = True

        if not randomize:
            fp = os.path.dirname(os.path.abspath(__file__))
            filename = os.getenv("FILENAME", None)

            with open(os.path.join(fp, filename), 'r') as f:
                try:
                    data = json.load(f)
                    board_state = np.array(data.get(pattern, None))
                    self.height, self.width = board_state.shape
                except:
                    print("Couldn't load selected grid layout from file, pattern: {},"
                          " file location: {}".format(pattern, (os.path.join(fp, filename))))
                    sys.exit(1)

        else:
            self.height = abs(height)
            self.width = abs(width)
            board_state = np.zeros((self.height, self.width))
            # Initialize a board with a random state
            for row in range(self.height):
                for col in range(self.width):
                    board_state[row][col] = random.randint(0, 1)

        self.temp_board = np.zeros((board_state.shape[0], board_state.shape[1]))
        self.init_board = board_state
        self.render(self.init_board, 0)

    def run_game(self):
        i = 1
        while self.listen:
            self.next_board_state(i)
            self.render(self.new_board, i)
            i += 1

    def next_board_state(self, cycle):
        if cycle == 1:
            board_state = self.init_board
            self.check_neighbors(board_state)
        else:
            board_state = self.new_board
            self.check_neighbors(board_state)

    def check_neighbors(self, board):
        board_state_test = board
        for row in range(0, self.height):
            for col in range(0, self.width):
                live_neighbors = 0

                # check if there is a row underneath the current
                if -1 < row + 1 <= self.height - 1:
                    live_neighbors += board_state_test[row + 1][col]
                    # underneath and behind (if there is a col behind)
                    if -1 < col - 1 <= self.width - 1:
                        live_neighbors += board_state_test[row + 1][col - 1]
                    # underneath and ahead (if there is a col ahead)
                    if -1 < col + 1 <= self.width - 1:
                        live_neighbors += board_state_test[row + 1][col + 1]

                # check if there is a row above the current
                if -1 < row - 1 <= self.height - 1:
                    live_neighbors += board_state_test[row - 1][col]
                    # above and behind
                    if -1 < col - 1 <= self.width - 1:
                        live_neighbors += board_state_test[row - 1][col - 1]
                    # above and ahead
                    if -1 < col + 1 <= self.width - 1:
                        live_neighbors += board_state_test[row - 1][col + 1]

                # check for adjacent cells
                if -1 < col - 1 <= self.width - 1:
                    live_neighbors += board_state_test[row][col - 1]
                if -1 < col + 1 <= self.width - 1:
                    live_neighbors += board_state_test[row][col + 1]

                self.gol_rules(
                               live_neighbors,
                               board_state_test,
                               row,
                               col
                               )

    def gol_rules(self, live_neighbors, board, row, col):
        """
           Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
           Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right
           Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
           Any dead cell with exactly 3 live neighbors becomes alive, by reproduction
        """
        current_cell_value = board[row][col]
        if current_cell_value > 0:
            if live_neighbors <= 1:
                self.temp_board[row][col] = 0
            elif 2 <= live_neighbors <= 3:
                self.temp_board[row][col] = current_cell_value
            elif live_neighbors > 3:
                self.temp_board[row][col] = 0
        else:
            if live_neighbors == 3:
                self.temp_board[row][col] = 1
            else:
                self.temp_board[row][col] = 0

        # check if we went through the whole grid
        if (row + 1 == board.shape[0]) and (col + 1 == board.shape[1]):
            self.new_board = self.temp_board

    def render(self, board, run):
        # TODO : Make UI to display the grid instead of '.' and '@'
        visual_matrix = np.empty((self.height, self.width), dtype=str)
        for row in range(0, self.height):
            for col in range(0, self.width):
                if board[row][col] == 1:
                    visual_matrix[row][col] = "@"
                else:
                    visual_matrix[row][col] = " "

        # setup curses
        stdscr = curses.initscr()
        stdscr.clear()
        stdscr.refresh()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_GREEN)

        title = 'Run #{}\n'.format(run)

        stdscr.attron(curses.color_pair(1))
        stdscr.attron(curses.A_BOLD)

        stdscr.addstr(title)

        # Make string of lists
        str_mat = '\n'.join(' '.join(sublist) for sublist in visual_matrix)
        stdscr.addstr(str_mat)

        stdscr.attroff(curses.color_pair(1))
        stdscr.attroff(curses.A_BOLD)

        stdscr.refresh()
        time.sleep(0.8)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, default=4, help="width of random grid layout")
    parser.add_argument('-he', type=int, default=4, help="height of random grid layout")
    parser.add_argument('-p', type=str, help="specify pattern to use from grid file, must be used with '-r' param")
    parser.add_argument('-r', action='store_false', help="turn random initialization of the grid off, by default on")
    args = parser.parse_args()

    game = GameOfLife(height=args.he, width=args.w, randomize=args.r, pattern=args.p)
    game.run_game()