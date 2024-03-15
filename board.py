import numpy as np
from dipole import Dipole
from historymanager import HistoryManager
import random
from generator import IGenerator
from dipole import State
from calculator import calc_all_probs


class Board:
    def __init__(self, size_x, size_y, flip_probability, generator: IGenerator):
        self.size_x = size_x
        self.size_y = size_y
        self.flip_probability = flip_probability
        self.history_manager = HistoryManager()
        self.grid = np.zeros((size_x, size_y), dtype=Dipole)
        self.initialize_grid()
        self.generator = generator

        # Record initial board state
        self.history_manager.record_board(self.get_committed_states())


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

        changed_dipoles = self.get_changed_dipoles()
        for dd in changed_dipoles:
            dd.commit_flip()

            for i in range(self.size_x):
                for j in range(self.size_y):
                    if self.grid[i, j] not in changed_dipoles:
                        number = self.generator.get_random()
                        self.grid[i,j].propagate(number)

        # Update history
        self.history_manager.record_writes(changed_dipoles)
        self.history_manager.record_board(self.get_committed_states())

    def is_changed(self) -> bool:
        return len(self.get_changed_dipoles()) > 0

    def get_changed_dipoles(self) -> list:
        changed = []
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.grid[i, j].dirty or self.grid[i, j].reinforced:
                    changed.append(self.grid[i, j])
        return changed