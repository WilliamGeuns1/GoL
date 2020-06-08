from GoL.game import GameOfLife
import numpy as np

def test_board_state():
    mock_board = np.array([[1, 0, 0, 1],
                          [0, 1, 1, 0],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1]])
    board = GameOfLife(height=4, width=4, randomize=True, pattern=None)

    expected =  np.array([[0, 0, 1, 0],
                          [0, 0, 0, 1],
                          [0, 0, 1, 0],
                          [0, 0, 0, 0]])

    actual = board.next_board_state(current_board=mock_board)

    assert actual.all() == expected.all()

def test_rules_no_change():
    mock_board = np.array([[1, 0, 0, 1],
                           [0, 1, 1, 0],
                           [1, 1, 0, 1],
                           [1, 1, 0, 1]])

    board = GameOfLife(height=4, width=4, randomize=True, pattern=None)
    actual = board.gol_rules(live_neighbors=4, board=mock_board, row=1, col=0)

    assert actual.all() == mock_board.all()

def test_rules_change():
    mock_board = np.array([[1, 0, 0, 1],
                           [0, 1, 1, 0],
                           [1, 1, 0, 1],
                           [1, 1, 0, 1]])

    expected = np.array([[1, 1, 0, 1],
                         [0, 1, 1, 0],
                         [1, 1, 0, 1],
                         [1, 1, 0, 1]])

    game = GameOfLife(height=4, width=4, randomize=True, pattern=None)
    actual = game.gol_rules(live_neighbors=3, board=mock_board, row=0, col=1)

    assert actual.all() == expected.all()


