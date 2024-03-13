from enum import Enum
import random


class State(Enum):
    UNKNOWN = 0
    OFF = 1
    ON = 2

class Dipole:
    def __init__(self, x, y, dirty=False):
        self.x = x
        self.y = y
        self.current_state = State.UNKNOWN
        self.proposed_state = State.UNKNOWN
        self.dirty = dirty
        self.prob_on = 0.0
        self.prob_off = 0.0
        self.prob_unchanged = 0.0

    def clear_probs(self):
        self.prob_on = 0
        self.prob_off = 0

    def cycle_stage_flip(self):
        self.proposed_state = State((self.proposed_state.value + 1) % len(State))
        self.determine_if_dirty()

    # If calling from command line, make_dirty is set to false so that if we are actually changing the state
    # then dirty is true, and if we are just reinforcing by writing the same state we still set dirty to true. 
    # It's a bit hacky and I don't like it - but it works for now
    def stage_flip(self, state: State, make_dirty=False):
        self.proposed_state = state
        if make_dirty:
            self.dirty = True
        else:
            self.determine_if_dirty()

    # Method called when right clicking in GUI. Whether a bit is truly dirty or not is not relevant.
    # If a bit is OFF, and we write OFF to it again, we are doing a "Reinforce" operation and this bit
    # should be treated as if it has just been written to. Reinforce operations always mean that the 
    # proposed state is the same as the current state
    def set_dirty(self):
        self.dirty = True
        self.proposed_state = self.current_state

    def determine_if_dirty(self):
        if (self.proposed_state != self.current_state):
            self.dirty = True
        else:
            self.dirty = False

    def set_current_state(self, state):
        self.current_state = state
        self.proposed_state = self.current_state

    def commit_flip(self):
        if (self.dirty):
            self.current_state = self.proposed_state
            self.dirty = False

    def reset_dirty(self):
        self.dirty = False

    

    def propagate(self) -> None:
        x = random.random()
        if x <= self.prob_off:
            self.set_current_state(State.OFF)

        elif self.prob_off < x <= self.prob_off + self.prob_on:
            self.set_current_state(State.ON)
