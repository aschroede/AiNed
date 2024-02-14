import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

class Dipole:
    def __init__(self, state=0, dirty = False):
        self.state = state
        self.dirty = dirty

    def flip(self):
        self.state = 1 - self.state
        self.dirty = True

    def reset_dirty(self):
        self.dirty = False

class Board:
    def __init__(self, size_x, size_y, flip_probability):
        self.size_x = size_x
        self.size_y = size_y
        self.flip_probability = flip_probability
        self.grid = np.zeros((size_x, size_y), dtype=Dipole)

    def initialize_grid(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid[i, j] = Dipole()

    def display(self):
        states = self.get_states()

        self.fig, self.ax = plt.subplots()

        self.im = self.ax.imshow(self.get_states(), cmap='binary', origin='lower', extent=[0, self.size_x, 0, self.size_y])
        plt.grid(True, color='blue', linewidth=1)
        plt.xticks(np.arange(0, self.size_x + 1, 1))
        plt.yticks(np.arange(0, self.size_y + 1, 1))
        plt.gca().set_aspect('equal', adjustable='box')

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.propagate_button = Button(plt.axes([0.8, 0.01, 0.15, 0.05]), 'Propagate')
        self.propagate_button.on_clicked(self.propagate_step)

        plt.show()

    def get_states(self):
        states = np.zeros((self.size_x, self.size_y))
        for i in range(self.size_x):
            for j in range(self.size_y):
                states[i, j] = self.grid[i, j].state
        return states

    def flip_dipole(self, x, y):
        self.grid[x, y].flip()
        # if np.random.rand() < self.flip_probability:
        #     self.covariant_flip(x, y)

    def write_step(self, x, y):
        self.grid[x, y].flip()
        self.update_display()

    def clear_dirty_bits(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.grid[i, j].reset_dirty()

    def propagate_step(self, event):
        # Calculate states of static dipoles based on dynamic dipoles and distance
        # Update self.grid accordingly
        self.clear_dirty_bits()
        self.update_display()

    def read_step(self):
        self.update_display()

    def update_display(self):
        states = self.get_states()
        self.im.set_array(states)

        # Create a list of colored rectangles for dirty dipoles
        dirty_patches = []
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.grid[i, j].dirty:
                    patch = plt.Rectangle((j, i), 1, 1, linewidth=3, edgecolor='red', facecolor='none')
                    dirty_patches.append(patch)

        # Clear the previous dirty patches and add the new ones
        for patch in getattr(self, '_dirty_patches', []):
            patch.remove()
        for patch in dirty_patches:
            self.ax.add_patch(patch)
        self._dirty_patches = dirty_patches

        self.fig.canvas.draw()
            

    def on_click(self, event):
        if event.inaxes == self.ax:
            x, y = int(event.xdata), int(event.ydata)

            # For some reason the x and y coordinates need to be swapped for 
            # clicking to work correctly. 
            self.write_step(y, x)

# Example usage
board = Board(size_x=8, size_y=8, flip_probability=0.2)
board.initialize_grid()
board.flip_dipole(1,1)


board.display()
