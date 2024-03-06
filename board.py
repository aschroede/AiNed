import numpy as np
from dipole import Dipole
from historymanager import HistoryManager
import random
from dipole import State


class Board:
    def __init__(self, size_x, size_y, flip_probability, history):
        self.size_x = size_x
        self.size_y = size_y
        self.flip_probability = flip_probability
        self.history_manager = history
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
            assert isinstance(dd, Dipole)
            self.history_manager.record_write(dd)

            for i in range(self.size_x):
                for j in range(self.size_y):
                    if self.grid[i, j] not in dirty_dipoles:
                        self.grid[i,j].propagate()

        self.history_manager.record_board(self.get_committed_states())

    def is_dirty(self) -> bool:
        return len(self.get_dirty_dipoles()) > 0

    def get_dirty_dipoles(self) -> list:
        dirty = []
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.grid[i, j].dirty == True:
                    dirty.append(self.grid[i, j])
        return dirty