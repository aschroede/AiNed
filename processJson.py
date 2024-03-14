import os
from jsonschema import validate
import json
from board import Board
from historymanager import HistoryManager
from dipole import Dipole, State
from calculator import calc_probs_examples


def load_and_validate_json(filename):
    base_dir = os.path.dirname(__file__)
    rel_path = "Data"
    schema_file_path = os.path.join(base_dir, rel_path, "jasonSchema.json")

    with open(schema_file_path) as schema_file:
        schema = json.load(schema_file)

    with open(filename, 'r') as data_file:
        data = json.load(data_file)

    validate(instance=data, schema=schema)

    return data


def process_board_data(data, output):
    board_properties = data["boardProperties"]
    rows = board_properties["rows"]
    columns = board_properties["columns"]
    prob = board_properties["probability"]
    timesteps = data["timesteps"]

    # Build board
    history_manager = HistoryManager()
    board = Board(size_x=rows, size_y=columns, flip_probability=prob, history=history_manager)

    # Apply changes for each timestep
    for timestep in timesteps:
        print(f"Time: {timestep['time']}, Changes: {timestep['changes']}")
        for change in timestep['changes']:
            x = change['x']
            y = change['y']
            proposed = change['state']
            current = board.get_dipole(x, y).current_state

            if proposed == current:
                # Reinforce operation
                board.get_dipole(x, y).reinforce()
            else:
                # Dirty operation (proposed state is different from current state)
                board.get_dipole(x, y).stage_flip(State(proposed))

        # Then calculate probabilities of flipping other dipoles
        calc_probs_examples(board)
        board.commit_and_propagate_staged_writes()

    board.history_manager.export_to_file(output)
