import random
import numpy as np

class GameOfLife():
    def __init__(self, height, width):
        self.listen = True
        self.height = height
        self.width = width

        board_state = np.zeros((height, width))
        # Initialize a board with a random state
        for col in range(self.width):
            for row in range(self.height):
                board_state[row][col] = random.randint(0, 1)

        self.board_state = board_state

        print(board_state.shape)


board = GameOfLife(5, 8)
    # def run_game(self):
    #     while self.listen:
    #         self.render(self.init_board)