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

        self.current_board = board_state
        self.temp_board = self.current_board.copy()


    def run_game(self):
        self.render(self.current_board)
        while self.listen:
            next_board_state = self.next_board_state(self.current_board)
            self.current_board = next_board_state.copy()
            self.render(self.current_board)

    def next_board_state(self, current_board):
        """
        This function calculates the next board state based on the current board state.

        Parameters:
            board     (np.array):   Current board state.

        Returns:
            new_board (np.array):   The new board state.
        """

        for row in range(0, self.height):
            for col in range(0, self.width):
                live_neighbors = 0
                # check if there is a row underneath the current
                if -1 < row + 1 <= self.height - 1:
                    live_neighbors += current_board[row + 1][col]
                    # underneath and behind (if there is a col behind)
                    if -1 < col - 1 <= self.width - 1:
                        live_neighbors += current_board[row + 1][col - 1]
                    # underneath and ahead (if there is a col ahead)
                    if -1 < col + 1 <= self.width - 1:
                        live_neighbors += current_board[row + 1][col + 1]

                # check if there is a row above the current
                if -1 < row - 1 <= self.height - 1:
                    live_neighbors += current_board[row - 1][col]
                    # above and behind
                    if -1 < col - 1 <= self.width - 1:
                        live_neighbors += current_board[row - 1][col - 1]
                    # above and ahead
                    if -1 < col + 1 <= self.width - 1:
                        live_neighbors += current_board[row - 1][col + 1]

                # check for adjacent cells
                if -1 < col - 1 <= self.width - 1:
                    live_neighbors += current_board[row][col - 1]
                if -1 < col + 1 <= self.width - 1:
                    live_neighbors += current_board[row][col + 1]

                new_board = self.gol_rules(live_neighbors, current_board, row, col)
        return new_board

    def gol_rules(self, live_neighbors, board, row, col):
        """
        This function applies the GoL rules stated below.

        Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation.
        Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right.
        Any live cell with more than 3 live neighbors becomes dead, because of overpopulation.
        Any dead cell with exactly 3 live neighbors becomes alive, by reproduction.

        Parameters:
            live_neighbors (int):   Number of alive neighbors.
            board     (np.array):   Current board state.
            row            (int):   Current row value.
            row            (int):   Current column value.

        Returns:
            temp_board (np.array): The updated board state.

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

        return self.temp_board

    def render(self, board):
        # TODO : Make UI to display the grid instead of ' ' and '@'
        visual_matrix = np.empty((self.height, self.width), dtype=str)
        for row in range(0, self.height):
            for col in range(0, self.width):
                if board[row][col] == 1:
                    visual_matrix[row][col] = "@"
                else:
                    visual_matrix[row][col] = " "

        # setup curses
        screen = curses.initscr()
        screen.clear()
        screen.refresh()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_GREEN)

        title = 'GoL\n'

        screen.attron(curses.color_pair(1))
        screen.attron(curses.A_BOLD)

        screen.addstr(title)

        # Make string of lists (board)
        str_mat = '\n'.join(' '.join(sublist) for sublist in visual_matrix)
        screen.addstr(str_mat)

        screen.attroff(curses.color_pair(1))
        screen.attroff(curses.A_BOLD)

        screen.refresh()
        time.sleep(0.40)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int, default=4, help="width of random grid layout")
    parser.add_argument('-he', type=int, default=4, help="height of random grid layout")
    parser.add_argument('-p', type=str, help="specify pattern to use from grid file, must be used with '-r' param")
    parser.add_argument('-r', action='store_false', default=True, help="turn random initialization of the grid off, by default on")
    args = parser.parse_args()

    game = GameOfLife(height=args.he, width=args.w, randomize=args.r, pattern=args.p)
    game.run_game()