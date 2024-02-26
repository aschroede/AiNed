from numpy.testing import assert_array_equal
from board import Board
import numpy as np
from dipole import Dipole
import utils


def test_get_proposed_states_zeros():
    board = Board(2, 2, 0.7)
    actual = board.get_proposed_states()
    expected = np.zeros((2, 2))
    assert_array_equal(actual, expected)


def test_stage_and_commit_changes():
    board = Board(2, 2, 0.7)
    actual = board.get_committed_states()
    expected = np.zeros((2, 2))
    assert_array_equal(actual, expected)

    # Write a change
    board.stage_write(1, 1)
    actual = board.get_committed_states()
    assert_array_equal(actual, expected)

    # Commit change
    board.commit_staged_writes()
    actual = board.get_committed_states()
    expected = np.zeros((2, 2))
    expected[1, 1] = 1
    assert_array_equal(actual, expected)


def test_stage_write():
    board = Board(2, 2, 0.7)
    board.stage_write(0, 0)
    expected = np.zeros((2, 2))
    expected[0, 0] = 1
    assert_array_equal(board.get_proposed_states(), expected)


def test_board_dirty():
    board = Board(2, 2, 0.7)
    assert not board.is_dirty()
    board.stage_write(0,0)
    assert board.is_dirty()
