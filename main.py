from board import Board
from display import Display
from number_gen import generate_random_numbers
from historymanager import HistoryManager
import typer
from processJson import process_board_data, load_and_validate_json
from generator import RandomIntGenerator, FileRandomGenerator
from typing_extensions import Annotated
from typing import Optional

app = typer.Typer()


@app.command()
def process_file(
        input_file: Annotated[str, typer.Argument(help="File path to JSON file to process.")],
        output_file: Annotated[str, typer.Argument(help="File path to save results to.")],
        random_file: Annotated[Optional[str], typer.Argument(help="File with random numbers to use for file processing. Note that such a file can be generated using the generatenumbes command")]):
    """
    Read in a json file (input) with a board properties and a series of writes. Save results to output.
    """
    random_generator = None
    if random_file is None:
        random_generator = RandomIntGenerator(0, 100, 123456)
    else:
        random_generator = FileRandomGenerator(random_file)

    data = load_and_validate_json(input_file)
    process_board_data(data, output_file, random_generator)

@app.command()
def generate_numbers(
        count: Annotated[int, typer.Argument(help="Number of random numbers to generate.")],
        filepath: Annotated[str, typer.Argument(help="File to save the random numbers to.")]):
    """
    Generate a file with random numbers from 0 to 100. Used for reproducible results.
    """
    generate_random_numbers(count, filepath)

@app.command()
def gui(
        rows: Annotated[int, typer.Argument(help="Number of rows of the dipole grid.")],
        columns: Annotated[int, typer.Argument(help="Number of columns of the dipole grid.")],
        probability: Annotated[float, typer.Option(help="Strength of co-varying effect")] = 0.7,
        seed: Annotated[int, typer.Option(help="Seed to use for random numbers")] = 123456):
    """
    Create a visual representation of the dipole grid that you can interact with via a GUI.
    """
    number_generator = RandomIntGenerator(0, 100, seed)
    board = Board(size_x=rows, size_y=columns, flip_probability=probability, generator=number_generator)
    Display(board)

if __name__ == "__main__":
    app()