from board import Board
from display import Display
from historymanager import HistoryManager
import typer
from jsonschema import validate
import json
import os

app = typer.Typer()



@app.command()
def initialize(
        rows: int,
        columns: int,
        probability: float = 0.7,
        output: str = None):

    history_manager = HistoryManager(output)
    board = Board(size_x=rows, size_y=columns, flip_probability=probability, history=history_manager)

@app.command()
def render():
    Display(board)


# if __name__ == "__main__":
#     app()



