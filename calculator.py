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


def calc_prob_example_1(dirty_dipoles: set, sink: Dipole, prob):
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


def calc_terms(dirty_dipoles: set, sink: Dipole, prob, pos_term = True):

    # First consider effect of first dirty dipole (B0 = ON)
    terms = []
    coefficients = []
    coefficients.append(1)
    for index, dipole in enumerate(dirty_dipoles):
        prob_on = calc_prob(dipole, sink, prob)
        coefficients.append((1 - prob_on) * coefficients[index])
        prob_on *= coefficients[index]
        terms.append(prob_on)

    return np.sum(terms)


def calc_probs_examples(board) -> None:
    # Calculate states of static dipoles based on dynamic dipoles and distance

    # Using the dirty bits, calculate if the static bits should change
    for i in range(board.size_x):
        for j in range(board.size_y):
            if not board.grid[i, j].dirty:
                dirty_dipoles = board.get_dirty_dipoles()

                positive_dipoles = set([dipole for dipole in dirty_dipoles if dipole.proposed_state == State.ON])
                negative_dipoles = set([dipole for dipole in dirty_dipoles if dipole.proposed_state == State.OFF])

                board.grid[i, j].clear_probs()

                if len(positive_dipoles) > 0 and len(negative_dipoles) == 0:
                    prob_pos = calc_terms(positive_dipoles, board.grid[i, j], board.flip_probability)
                    board.grid[i, j].prob_on = prob_pos
                    board.grid[i, j].prob_unchanged = 1-prob_pos

                elif len(positive_dipoles) == 0 and len(negative_dipoles) > 0:
                    prob_neg = calc_terms(negative_dipoles, board.grid[i, j], board.flip_probability)
                    board.grid[i, j].prob_off = prob_neg
                    board.grid[i, j].prob_unchanged = 1-prob_neg

                else:
                    pos_term = calc_terms(positive_dipoles, board.grid[i, j], board.flip_probability)
                    neg_term = calc_terms(negative_dipoles, board.grid[i, j], board.flip_probability)
                    prob_pos = pos_term*(1-neg_term)
                    prob_neg = neg_term*(1-pos_term)
                    board.grid[i, j].prob_on = prob_pos
                    board.grid[i, j].prob_off = prob_neg
                    board.grid[i, j].prob_unchanged = 1-prob_pos-prob_pos


