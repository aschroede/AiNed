from dipole import Dipole, State
import math
import numpy as np


def manhatten_distance(first: Dipole, second: Dipole):
    x_delta = abs(first.x - second.x)
    y_delta = abs(first.y - second.y)
    return x_delta + y_delta

def calc_prob(source: Dipole, sink: Dipole, prob, invert=False):
    distance = manhatten_distance(source, sink)
    if invert:
        return 1 - math.pow(prob, distance)
    return math.pow(prob, distance)

def calc_prob_new(dirty_dipoles: set, sink: Dipole, prob):

    # Calculate prob that sink is set to ON = 2

    # First consider effect of first dirty dipole (B0 = ON)
    terms = []
    for dipole in dirty_dipoles:
        if dipole.proposed_state == State.ON:
            prob_on = calc_prob(dipole, sink, prob)
            terms.append(prob_on)
        elif dipole.proposed_state == State.OFF:
            prob_on = calc_prob(dipole, sink, prob, invert=True)
            terms.append(prob_on)

    return np.prod(terms)

def calc_probs_example1(board) -> None:
    # Calculate states of static dipoles based on dynamic dipoles and distance

    # Using the dirty bits, calculate if the static bits should change
    for i in range(board.size_x):
        for j in range(board.size_y):
            if not board.grid[i, j].dirty:
                prob = calc_prob_new(board.get_dirty_dipoles(), board.grid[i, j], board.flip_probability)
                board.grid[i, j].prob = prob
