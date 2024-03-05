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

    def stage_flip(self, state: State):
        self.proposed_state = state
        self.determine_if_dirty()

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
