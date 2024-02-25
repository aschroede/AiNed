from numpy.testing import assert_array_equal
from board import Board
import numpy as np
from dipole import Dipole
import utils

board = Board(2, 2, 0.7)

def test_get_proposed_states_zeros():
    actual = board.get_proposed_states()
    expected = np.zeros((2, 2))
    assert_array_equal(actual, expected)

def test_stage_write():
    board = Board(2, 2, 0.7)
    board.stage_write(0,0)
    expected = np.zeros((2,2))
    expected[0, 0] = 1
    assert_array_equal(board.get_proposed_states(), expected)


































