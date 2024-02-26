from dipole import Dipole
import math

def manhatten_distance(first: Dipole, second: Dipole):
    x_delta = abs(first.x - second.x)
    y_delta = abs(first.y - second.y)
    return x_delta + y_delta

def calc_prob(source: Dipole, sink: Dipole, prob):
    distance = manhatten_distance(source, sink)
    return math.pow(prob, distance)