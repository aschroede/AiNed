from board import Board
from display import Display
from number_gen import generate_random_numbers
from historymanager import HistoryManager
import typer
from processJson import process_board_data, load_and_validate_json

app = typer.Typer()


@app.command()
def processFile(input: str, output: str):
    data = load_and_validate_json(input)
    process_board_data(data, output)

@app.command()
def generateNumbers(count: int, filepath: str):
    generate_random_numbers(count, filepath)

@app.command()
def gui(rows: int, columns: int, probability: float = 0.7):
    history_manager = HistoryManager()
    board = Board(size_x=rows, size_y=columns, flip_probability=probability, history=history_manager)
    Display(board)


if __name__ == "__main__":
    app()
