import matplotlib.pyplot as plt
import numpy as np
from board import Board
from matplotlib.widgets import Button
from matplotlib.colors import ListedColormap
from dipole import State
from calculator import calc_probs_example1

ON_COLOR = 'blue'
OFF_COLOR = 'red'
UNKNOWN_COLOR = 'black'
DIRTY_COLOR = 'purple'
TEXT_COLOR = 'white'


class Display:

    def __init__(self, board: Board):
        self.board = board
        self.fig, self.ax = plt.subplots()

        self.colors = [UNKNOWN_COLOR, OFF_COLOR, ON_COLOR]

        print(self.colors[1])
        self.cmap = ListedColormap(colors=self.colors)

        proposed_states = board.get_proposed_states()
        self.im = self.ax.imshow(board.get_proposed_states(), cmap=self.cmap, vmin=0, vmax=len(State) - 1,
                                 origin='lower',
                                 extent=[0, board.size_x, 0, board.size_y], interpolation='nearest')

        plt.grid(True, color=DIRTY_COLOR, linewidth=1)
        plt.xticks(np.arange(0, board.size_x + 1, 1))
        plt.yticks(np.arange(0, board.size_y + 1, 1))
        plt.gca().set_aspect('equal', adjustable='box')

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.propagate_button = Button(plt.axes([0.8, 0.01, 0.15, 0.05]), 'Commit Writes')
        self.propagate_button.on_clicked(self.commit_staged_writes)

        plt.show()

    def commit_staged_writes(self, event):
        self.board.commit_and_propagate_staged_writes()
        self.display_committed_writes()

    def clear_probs(self):
        self.ax.texts.clear()
        self.fig.canvas.draw()

    def display_probs(self):
        self.ax.texts.clear()  # Clear previous text annotations
        for i in range(self.board.size_x):
            for j in range(self.board.size_y):
                if (self.board.get_dipole(i, j).dirty == False):
                    self.ax.text(j + 0.5, i + 0.5, f'{self.board.get_dipole(i, j).prob:.2f}', ha='center', va='center',
                                 color=TEXT_COLOR,
                                 fontsize=8)
        self.fig.canvas.draw()

    def display_committed_writes(self):
        self.clear_probs()
        self.ax.patches.clear()
        states = self.board.get_committed_states()
        self.im.set_data(states)
        self.fig.canvas.draw()

    def display_staged_writes(self):
        self.ax.patches.clear()

        states = self.board.get_proposed_states()
        self.im.set_data(states)

        # Create a list of colored rectangles for dirty dipoles
        dirty_patches = []
        for i in range(self.board.size_x):
            for j in range(self.board.size_y):
                if self.board.get_dipole(i, j).dirty:
                    patch = plt.Rectangle((j, i), 1, 1, linewidth=3, edgecolor=DIRTY_COLOR, facecolor='none')
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
            self.board.get_dipole(y, x).cycle_stage_flip()
            self.display_staged_writes()

            # After flipping a bit we should calculate the probs and display them
            if (self.board.is_dirty()):
                calc_probs_example1(self.board)
                self.display_probs()
            else:
                self.clear_probs()
