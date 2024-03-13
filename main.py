from board import Board
from display import Display
from historymanager import HistoryManager
import typer
from jsonschema import validate
import json
import os
from processJson import process_board_data, load_json

app = typer.Typer()



@app.command()
def processfile(
        rows: int,
        columns: int,
        probability: float = 0.7,
        output: str = None):

    history_manager = HistoryManager(output)
    board = Board(size_x=rows, size_y=columns, flip_probability=probability, history=history_manager)
    # Assuming your JSON data is stored in 'board_data.json'
    data = load_json('exampleData.json')
    process_board_data(data, board)

@app.command()
def gui(
        rows: int,
        columns: int,
        probability: float = 0.7,
        output: str = None):

    history_manager = HistoryManager(output)
    board = Board(size_x=rows, size_y=columns, flip_probability=probability, history=history_manager)
    Display(board)


if __name__ == "__main__":
     app()



