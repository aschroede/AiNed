from numpy.testing import assert_array_equal
from board import Board
import numpy as np
from dipole import Dipole, State
from calculator import calc_probs_examples


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
    board.get_dipole(1,1).stage_flip(State.OFF)
    actual = board.get_committed_states()
    assert_array_equal(actual, expected)

    # Commit change
    board.commit_and_propagate_staged_writes()
    actual = board.get_committed_states()
    expected = np.zeros((2, 2))
    expected[1, 1] = 1
    assert_array_equal(actual, expected)


def test_stage_write():
    board = Board(2, 2, 0.7)
    board.get_dipole(0,0).stage_flip(State.OFF)
    expected = np.zeros((2, 2))
    expected[0, 0] = 1
    assert_array_equal(board.get_proposed_states(), expected)


def test_board_dirty():
    board = Board(2, 2, 0.7)
    assert not board.is_dirty()
    board.get_dipole(0,0).stage_flip(State.ON)
    assert board.is_dirty()


def test_propagate():
    board = Board(2, 2, 0.7)

    # First stage changes
    board.get_dipole(0,0).stage_flip(State.OFF)

    # Then calculate probabilities of flipping other dipoles
    calc_probs_examples(board)

    # Then commit the changes and propagate them
    board.commit_and_propagate_staged_writes()

    actual = board.get_committed_states()
    print(actual)
    expected = np.array([[1, 0], [1, 0]])
    assert_array_equal(actual, expected)
