# Purpose is to keep a record of changes that were written, and the resulting board state after propogation
from dipole import Dipole, State

class HistoryManager:

    def __init__(self):
        self.board_history = []
        self.write_history = []
        
    def record_board(self, board_state):
        self.board_history.append(board_state)
        
    def record_write(self, dipole: Dipole):
        info = (dipole.x, dipole.y, dipole.current_state)
        self.write_history.append(info)
    
    def clear_history(self):
        self.board_history.clear()
        self.write_history.clear()
        
    def save_history_to_file(self):
        pass