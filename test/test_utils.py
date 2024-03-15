import calculator
from board import Board
from dipole import Dipole, State
from math import isclose
from historymanager import HistoryManager


def test_manhatten_dist_zero():
    history_manager = HistoryManager()
    board = Board(2, 2, 0.7, history_manager)
    dist = calculator.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(0, 0))
    assert dist == 0


def test_manhatten_dist_one():
    history_manager = HistoryManager()
    board = Board(2, 2, 0.7, history_manager)
    dist = calculator.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(0, 1))
    assert dist == 1


def test_manhatten_dist_two():
    history_manager = HistoryManager()
    board = Board(2, 2, 0.7, history_manager)
    dist = calculator.manhatten_distance(board.get_dipole(0, 0), board.get_dipole(1, 1))
    assert dist == 2


def test_calc_prob_dist_one():
    history_manager = HistoryManager()
    board = Board(2, 2, 0.7, history_manager)
    prob = calculator.calc_prob(board.get_dipole(0, 0), board.get_dipole(0, 1), board.flip_probability)
    assert prob == 0.7


def test_calc_prob_dist_two():
    history_manager = HistoryManager()
    board = Board(2, 2, 0.7, history_manager)
    prob = calculator.calc_prob(board.get_dipole(0, 0), board.get_dipole(1, 1), board.flip_probability)
    assert isclose(prob, 0.49)

def test_calc_example_1():
    history_manager = HistoryManager()
    board = Board(2, 2, 0.7, history_manager)
    board.get_dipole(0, 0).stage_flip(State.ON)
    board.get_dipole(1, 1).stage_flip(State.OFF)
    calculator.calc_all_probs(board)
    assert isclose(board.get_dipole(0, 1).prob_on, 0.21)
    assert isclose(board.get_dipole(1, 0).prob_on, 0.21)
