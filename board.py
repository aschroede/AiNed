import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from dipole import Dipole

import random
import math
import time


class Board:
    def __init__(self, size_x, size_y, flip_probability):
        self.size_x = size_x
        self.size_y = size_y
        self.flip_probability = flip_probability
        self.grid = np.zeros((size_x, size_y), dtype=Dipole)
        self.dirty_dipoles = []

    def initialize_grid(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid[i, j] = Dipole(i, j)

    def display(self):
        self.fig, self.ax = plt.subplots()

        self.im = self.ax.imshow(self.get_proposed_states(), cmap='binary', origin='lower',
                                 extent=[0, self.size_x, 0, self.size_y])
        plt.grid(True, color='blue', linewidth=1)
        plt.xticks(np.arange(0, self.size_x + 1, 1))
        plt.yticks(np.arange(0, self.size_y + 1, 1))
        plt.gca().set_aspect('equal', adjustable='box')

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.propagate_button = Button(plt.axes([0.8, 0.01, 0.15, 0.05]), 'Commit Writes')
        self.propagate_button.on_clicked(self.commit_staged_writes)

        plt.show()

    def get_proposed_states(self):
        states = np.zeros((self.size_x, self.size_y))
        for i in range(self.size_x):
            for j in range(self.size_y):
                states[i, j] = self.grid[i, j].proposed_state
        return states

    def get_committed_states(self):
        states = np.zeros((self.size_x, self.size_y))
        for i in range(self.size_x):
            for j in range(self.size_y):
                states[i, j] = self.grid[i, j].current_state
        return states

    def flip_dipole(self, x, y):
        self.grid[x, y].flip()
        # if np.random.rand() < self.flip_probability:
        #     self.covariant_flip(x, y)

    def stage_write(self, x, y):
        # self.clear_dirty_bits()
        self.grid[x, y].stage_flip()

        if (self.grid[x, y].dirty):
            self.dirty_dipoles.append(self.grid[x, y])

        self.display_staged_writes()

        # After flipping a bit we should calculate the probs and display them
        if (self.board_dirty()):
            self.calc_probs()
            self.update_display_probs()
        else:
            self.clear_display_probs()

    def board_dirty(self):
        dirty = False
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.grid[i, j].dirty == True:
                    dirty = True
                    break
        return dirty

    def clear_dirty_bits(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid[i, j].reset_dirty()

    def calc_probs(self, simulate=False):
        # Calculate states of static dipoles based on dynamic dipoles and distance
        # Update self.grid accordingly

        sources = []

        # Collect all the dirty bits (dynamic bits)
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.grid[i, j].dirty:
                    sources.append(self.grid[i, j])

        # Using the dirty bits, calculate if the static bits should change
        for source in sources:
            for i in range(self.size_x):
                for j in range(self.size_y):
                    if self.grid[i, j].dirty == False:
                        self.calc_prob(source, self.grid[i, j])

        # self.update_display()

    def propogate(self, source: Dipole, sink: Dipole):
        if random.randint(0, 100) < (sink.prob) * 100:
            sink.set_current_state(source.current_state)

    def calc_prob(self, source: Dipole, sink: Dipole):

        distance = self.manhatten_distance(source, sink)
        sink.prob = math.pow(self.flip_probability, distance)

    def manhatten_distance(self, first: Dipole, second: Dipole):
        x_delta = abs(first.x - second.x)
        y_delta = abs(first.y - second.y)
        return x_delta + y_delta

    def read_step(self):
        self.display_staged_writes()

    def clear_display_probs(self):
        self.ax.texts.clear()
        self.fig.canvas.draw()

    def update_display_probs(self):
        self.ax.texts.clear()  # Clear previous text annotations
        for i in range(self.size_x):
            for j in range(self.size_y):
                if (self.grid[i, j].dirty == False):
                    self.ax.text(j + 0.5, i + 0.5, f'{self.grid[i, j].prob:.2f}', ha='center', va='center', color='red',
                                 fontsize=8)

        self.fig.canvas.draw()

    def commit_staged_writes(self, event):

        for dd in self.dirty_dipoles:
            dd.commit_flip()

            for i in range(self.size_x):
                for j in range(self.size_y):
                    if self.grid[i, j].dirty == False:
                        self.propogate(dd, self.grid[i, j])

        self.dirty_dipoles.clear()
        self.display_committed_writes()

    def display_committed_writes(self):
        self.clear_display_probs()
        self.ax.patches.clear()
        states = self.get_committed_states()
        self.im.set_array(states)
        self.im.set_clim(vmin=0, vmax=1)
        self.fig.canvas.draw()

    def display_staged_writes(self):

        states = self.get_proposed_states()
        self.im.set_array(states)
        self.im.set_clim(vmin=0, vmax=1)

        self.ax.patches.clear()

        # Create a list of colored rectangles for dirty dipoles
        dirty_patches = []
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.grid[i, j].dirty:
                    patch = plt.Rectangle((j, i), 1, 1, linewidth=3, edgecolor='red', facecolor='none')
                    dirty_patches.append(patch)

        # Clear the previous dirty patches and add the new ones
        for patch in dirty_patches:
            self.ax.add_patch(patch)

        self.fig.canvas.draw()

    def on_click(self, event):
        if event.inaxes == self.ax:
            x, y = int(event.xdata), int(event.ydata)

            # For some reason the x and y coordinates need to be swapped for 
            # clicking to work correctly. 
            self.stage_write(y, x)