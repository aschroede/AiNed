class Dipole:
    def __init__(self, x, y, state=0, dirty = False):
        self.x = x
        self.y = y
        self.current_state = state
        self.dirty = dirty
        self.prob = 0.0
        self.proposed_state = state

    def stage_flip(self):
        self.proposed_state = 1 - self.proposed_state

        if (self.proposed_state != self.current_state):
            self.dirty = True
        else:
            self.dirty = False

    def set_current_state(self, state):
        self.current_state = state
        self.proposed_state = self.current_state

    def commit_flip(self):
        if(self.dirty):
            self.current_state = self.proposed_state
            self.dirty = False

    def reset_dirty(self):
        self.dirty = False