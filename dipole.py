from enum import Enum


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
        self.prob = 0.0

    def stage_flip(self):
        self.proposed_state = State((self.proposed_state.value + 1) % len(State))

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
