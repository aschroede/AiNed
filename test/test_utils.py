import calculator
from board import Board
from dipole import Dipole, State
from math import isclose


def test_manhatten_dist_zero():
    board = Board(2, 2, 0.7)
    dist = calculator.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(0, 0))
    assert dist == 0


def test_manhatten_dist_one():
    board = Board(2, 2, 0.7)
    dist = calculator.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(0, 1))
    assert dist == 1


def test_manhatten_dist_two():
    board = Board(2, 2, 0.7)
    dist = calculator.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(1, 1))
    assert dist == 2


def test_calc_prob_dist_one():
    board = Board(2, 2, 0.7)
    prob = calculator.calc_prob(board.get_dipole(0, 0), board.get_dipole(0, 1), board.flip_probability)
    assert prob == 0.7


def test_calc_prob_dist_two():
    board = Board(2, 2, 0.7)
    prob = calculator.calc_prob(board.get_dipole(0, 0), board.get_dipole(1, 1), board.flip_probability)
    assert isclose(prob, 0.49)

def test_calc_example_1():
    board = Board(2, 2, 0.7)
    board.get_dipole(0, 0).stage_flip(State.ON)
    board.get_dipole(1, 1).stage_flip(State.OFF)
    calculator.calc_probs_examples(board)
    assert isclose(board.get_dipole(0, 1).prob, 0.21)
    assert isclose(board.get_dipole(1, 0).prob, 0.21)
