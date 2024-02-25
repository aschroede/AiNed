from numpy.testing import assert_array_equal
from board import Board
import numpy as np
from math import isclose
from dipole import Dipole
import utils


def test_initial_test():
    board = Board(8, 8, 0.7)
    board.initialize_grid()
    actual = board.get_proposed_states()
    expected = np.zeros((8, 8))
    assert_array_equal(actual, expected)


board = Board(2, 2, 0.7)


def test_manhatten_dist_zero():
    dist = utils.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(0, 0))
    assert dist == 0


def test_manhatten_dist_one():
    dist = utils.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(0, 1))
    assert dist == 1


def test_manhatten_dist_two():
    dist = utils.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(1, 1))
    assert dist == 2


def test_calc_prob_dist_one():
    prob = utils.calc_prob(board.get_dipole(0, 0), board.get_dipole(0, 1), board.flip_probability)
    assert prob == 0.7


def test_calc_prob_dist_two():
    prob = utils.calc_prob(board.get_dipole(0, 0), board.get_dipole(1, 1), board.flip_probability)
    assert isclose(prob, 0.49)


