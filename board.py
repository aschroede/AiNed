import numpy as np
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from dipole import Dipole
from calculator import calc_prob

import random
import math
import time


class Board:
    def __init__(self, size_x, size_y, flip_probability):
        self.size_x = size_x
        self.size_y = size_y
        self.flip_probability = flip_probability
        self.__grid = np.zeros((size_x, size_y), dtype=Dipole)
        self.dirty_dipoles = []
        self.initialize_grid()
        random.seed(1234567)

    def initialize_grid(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.__grid[i, j] = Dipole(i, j)

    def get_dipole(self, x, y):
        return self.__grid[x, y]

    def get_proposed_states(self):
        states = np.zeros((self.size_x, self.size_y))
        for i in range(self.size_x):
            for j in range(self.size_y):
                states[i, j] = self.__grid[i, j].proposed_state
        return states

    def get_committed_states(self):
        states = np.zeros((self.size_x, self.size_y))
        for i in range(self.size_x):
            for j in range(self.size_y):
                states[i, j] = self.__grid[i, j].current_state
        return states

    def stage_write(self, x, y):
        self.__grid[x, y].stage_flip()
        if (self.__grid[x, y].dirty):
            self.dirty_dipoles.append(self.__grid[x, y])

    def commit_and_propagate_staged_writes(self):

        for dd in self.dirty_dipoles:
            dd.commit_flip()

            for i in range(self.size_x):
                for j in range(self.size_y):
                    if self.__grid[i, j].dirty == False:
                        self.propogate(dd, self.__grid[i, j])

        self.dirty_dipoles.clear()

    def is_dirty(self):
        return len(self.dirty_dipoles) > 0

    def propogate(self, source: Dipole, sink: Dipole):
        if random.randint(0, 100) < (sink.prob) * 100:
            sink.set_current_state(source.current_state)

    # region Calculations

    def calc_probs(self, simulate=False):
        # Calculate states of static dipoles based on dynamic dipoles and distance

        # Using the dirty bits, calculate if the static bits should change
        for source in self.dirty_dipoles:
            for i in range(self.size_x):
                for j in range(self.size_y):
                    if self.__grid[i, j].dirty == False:
                        prob = calc_prob(source, self.__grid[i, j], self.flip_probability)
                        self.__grid[i, j].prob = prob
    # endregion
