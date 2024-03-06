from board import Board
from display import Display
from historymanager import HistoryManager


history_manager = HistoryManager()
board = Board(size_x=8, size_y=8, flip_probability=0.7, history=history_manager)
display = Display(board)

