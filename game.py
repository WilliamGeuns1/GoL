import os
import random
import time
import json
import numpy as np

class GameOfLife():
    def __init__(self, height=None, width=None, randomize=True):
        self.listen = True


        if not randomize:
            fp = os.path.dirname(os.path.abspath(__file__))
            filename=os.getenv("FILENAME", None)
            with open(os.path.join(fp, filename), 'r') as f:
                data = json.load(f)
                board_state = np.array(data.get("test1", None))
                self.height, self.width = board_state.shape

        else:
            self.height = abs(height)
            self.width = abs(width)
            board_state = np.zeros((height, width))
            # Initialize a board with a random state
            for row in range(self.height):
                for col in range(self.width):
                    board_state[row][col] = random.randint(0, 1)

        self.new_board = np.zeros((self.height, self.width))
        self.init_board = board_state
        print("Initial board")
        self.render(self.init_board)

    def run_game(self):
        i = 0
        while self.listen:
            self.next_board_state(i)
            self.render(self.new_board)
            i += 1

    def next_board_state(self, cycle):
        print("Run {}".format(cycle))
        if cycle == 0:
            board = self.init_board
        else:
            board = self.new_board

        for row in range(0, self.height):
            for col in range(0, self.width):
                live_neighbors = 0
                # check if there is a row underneath the current
                if -1 < row + 1 <= self.height - 1:
                    live_neighbors += board[row + 1][col]
                    # underneath and behind (if there is a col behind)
                    if -1 < col - 1 <= self.width - 1:
                        live_neighbors += board[row + 1][col - 1]
                    # underneath and ahead (if there is a col ahead)
                    if -1 < col + 1 <= self.width - 1:
                        live_neighbors += board[row + 1][col + 1]

                # check if there is a row above the current
                if -1 < row - 1 <= self.height - 1:
                    live_neighbors += board[row - 1][col]
                    # above and behind
                    if -1 < col - 1 <= self.width - 1:
                        live_neighbors += board[row - 1][col - 1]
                    # above and ahead
                    if -1 < col + 1 <= self.width - 1:
                        live_neighbors += board[row - 1][col + 1]

                # check for adjacent cells
                if -1 < col - 1 <= self.width - 1:
                    live_neighbors += board[row][col - 1]
                if -1 < col + 1 <= self.width - 1:
                    live_neighbors += board[row][col + 1]

                self.gol_rules(live_neighbors,
                               board,
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
                self.new_board[row][col] = 0
            elif 2 <= live_neighbors <= 3:
                self.new_board[row][col] = current_cell_value
            elif live_neighbors > 3:
                self.new_board[row][col] = 0
        else:
            if live_neighbors == 3:
                self.new_board[row][col] = 1

    def render(self, board):
        visual_matrix = np.empty((self.height, self.width), dtype=str)
        for row in range(0, self.height):
            for col in range(0, self.width):
                if board[row][col] == 1:
                    visual_matrix[row][col] = "@"
                else:
                    visual_matrix[row][col] = "."
        # print("\033[1;32;")
        print("{}".format(visual_matrix))
        time.sleep(2)


if __name__ == '__main__':
    game = GameOfLife(randomize=False)
    game.run_game()