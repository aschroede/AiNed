import calculator
from board import Board
from math import isclose


board = Board(2, 2, 0.7)
def test_manhatten_dist_zero():
    dist = calculator.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(0, 0))
    assert dist == 0


def test_manhatten_dist_one():
    dist = calculator.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(0, 1))
    assert dist == 1


def test_manhatten_dist_two():
    dist = calculator.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(1, 1))
    assert dist == 2


def test_calc_prob_dist_one():
    prob = calculator.calc_prob(board.get_dipole(0, 0), board.get_dipole(0, 1), board.flip_probability)
    assert prob == 0.7


def test_calc_prob_dist_two():
    prob = calculator.calc_prob(board.get_dipole(0, 0), board.get_dipole(1, 1), board.flip_probability)
    assert isclose(prob, 0.49)