import numpy as np
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from dipole import Dipole
from calculator import calc_prob, calc_prob_new
import random
from dipole import State


class Board:
    def __init__(self, size_x, size_y, flip_probability):
        self.size_x = size_x
        self.size_y = size_y
        self.flip_probability = flip_probability
        self.grid = np.zeros((size_x, size_y), dtype=Dipole)
        self.initialize_grid()
        random.seed(1234567)

    def initialize_grid(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid[i, j] = Dipole(i, j)

    def get_dipole(self, x, y) -> Dipole:
        return self.grid[x, y]

    def get_proposed_states(self) -> np.ndarray:
        states = np.full((self.size_x, self.size_y), 0, dtype=int)
        for i in range(self.size_x):
            for j in range(self.size_y):
                states[i, j] = int(self.grid[i, j].proposed_state.value)
        return states

    def get_committed_states(self) -> np.ndarray:
        states = np.zeros((self.size_x, self.size_y))
        for i in range(self.size_x):
            for j in range(self.size_y):
                states[i, j] = self.grid[i, j].current_state.value
        return states

    def commit_and_propagate_staged_writes(self) -> None:
        dirty_dipoles = self.get_dirty_dipoles()
        for dd in dirty_dipoles:
            dd.commit_flip()

            for i in range(self.size_x):
                for j in range(self.size_y):
                    if self.grid[i, j].dirty == False:
                        self.propogate(dd, self.grid[i, j])

    def is_dirty(self) -> bool:
        return len(self.get_dirty_dipoles()) > 0

    def get_dirty_dipoles(self) -> list:
        dirty = []
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.grid[i, j].dirty == True:
                    dirty.append(self.grid[i, j])
        return dirty

    def propogate(self, source: Dipole, sink: Dipole) -> None:
        if random.randint(0, 100) < (sink.prob) * 100:
            sink.set_current_state(source.current_state)

    def calc_probs(self, simulate=False) -> None:
        # Calculate states of static dipoles based on dynamic dipoles and distance

        # Using the dirty bits, calculate if the static bits should change
        for source in self.get_dirty_dipoles():
            for i in range(self.size_x):
                for j in range(self.size_y):
                    if self.grid[i, j].dirty == False:
                        prob = calc_prob(source, self.grid[i, j], self.flip_probability)
                        self.grid[i, j].prob = prob
