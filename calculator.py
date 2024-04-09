from dipole import Dipole, State
import math
import numpy as np
from fxpmath import Fxp

DTYPE = "fxp-u16/16"

def manhatten_distance(first: Dipole, second: Dipole):
    x_delta = abs(first.x - second.x)
    y_delta = abs(first.y - second.y)
    return x_delta + y_delta


def calc_prob(source: Dipole, sink: Dipole, prob: Fxp):

    # Ensure inputs are fixed point
    assert prob.dtype == DTYPE

    distance = manhatten_distance(source, sink)
    power = Fxp(None, False, dtype=DTYPE)
    power.equal(prob ** Fxp(distance))

    # Ensure output is fixed point
    assert power.dtype == DTYPE

    return power


def calc_terms(dirty_dipoles: set, sink: Dipole, prob, pos_term = True):

    terms = []
    coefficients = []

    initial = Fxp(1, False, dtype=DTYPE)

    coefficients.append(initial)

    for index, dipole in enumerate(dirty_dipoles):
        prob_on = calc_prob(dipole, sink, prob)
        one = Fxp(1, False, dtype=DTYPE)
        coefficients.append((one - prob_on) * coefficients[index])
        prob_on *= coefficients[index]
        terms.append(prob_on)

    sum = Fxp(None, False, dtype=DTYPE)
    sum.equal(np.sum(terms))

    assert sum.dtype == DTYPE
    return sum


def calc_all_probs(board) -> None:
    # Calculate states of static dipoles based on dynamic dipoles and distance

    # Using the dirty bits, calculate if the static bits should change
    for i in range(board.size_x):
        for j in range(board.size_y):
            if not board.grid[i, j].dirty:
                changed_dipoles = board.get_changed_dipoles()

                positive_dipoles = set([dipole for dipole in changed_dipoles if dipole.proposed_state == State.ON])
                negative_dipoles = set([dipole for dipole in changed_dipoles if dipole.proposed_state == State.OFF])

                board.grid[i, j].clear_probs()

                one = Fxp(1, False, dtype=DTYPE)

                if len(positive_dipoles) > 0 and len(negative_dipoles) == 0:
                    prob_pos = calc_terms(positive_dipoles, board.grid[i, j], board.flip_probability)
                    board.grid[i, j].prob_on = prob_pos

                    result = Fxp(None, False, dtype=DTYPE)
                    result.equal(one-prob_pos)
                    board.grid[i, j].prob_unchanged = result

                elif len(positive_dipoles) == 0 and len(negative_dipoles) > 0:
                    prob_neg = calc_terms(negative_dipoles, board.grid[i, j], board.flip_probability)
                    board.grid[i, j].prob_off = prob_neg

                    result = Fxp(None, False, dtype=DTYPE)
                    result.equal(one-prob_neg)
                    board.grid[i, j].prob_unchanged = result

                else:
                    pos_term = calc_terms(positive_dipoles, board.grid[i, j], board.flip_probability)
                    neg_term = calc_terms(negative_dipoles, board.grid[i, j], board.flip_probability)

                    result = Fxp(None, False, dtype=DTYPE)
                    result.equal(pos_term*(one-neg_term))
                    prob_pos = result
                    
                    result = Fxp(None, False, dtype=DTYPE)
                    result.equal(neg_term*(one-pos_term))
                    prob_neg = result


                    board.grid[i, j].prob_on = prob_pos
                    board.grid[i, j].prob_off = prob_neg

                    result = Fxp(None, False, dtype=DTYPE)
                    result.equal(one-prob_pos-prob_neg)
                    assert result.dtype == DTYPE

                    board.grid[i, j].prob_unchanged = result


