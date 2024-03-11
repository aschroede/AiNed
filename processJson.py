import json
import os
from jsonschema import validate
import json
from board import Board
from historymanager import HistoryManager
from dipole import Dipole, State
from calculator import calc_probs_examples



def load_json(filename):
    base_dir = os.path.dirname(__file__)
    rel_path = "Data"
    schema_file_path = os.path.join(base_dir, rel_path, "jasonSchema.json")
    data_file_path = os.path.join(base_dir, rel_path, filename)

    with open(schema_file_path) as schema_file:
        schema = json.load(schema_file)

    with open(data_file_path, 'r') as data_file:
        data = json.load(data_file)

    validate(instance=data, schema=schema)

    return data

def process_board_data(data):
    board_properties = data["boardProperties"]
    rows = board_properties["rows"]
    columns = board_properties["columns"]
    prob = board_properties["probability"]

    history_manager = HistoryManager("test.txt")
    board = Board(size_x=rows, size_y=columns, flip_probability=prob, history=history_manager)


    timesteps = data["timesteps"]
    
    # Example processing: print board properties and timesteps
    print("Board Properties:", board_properties)
    for timestep in timesteps:
        print(f"Time: {timestep['time']}, Changes: {timestep['changes']}")

        for change in timestep['changes']:
            x = change['x']
            y = change['y']
            state = change['state']
            board.get_dipole(x, y).stage_flip(State(state))

        # Then calculate probabilities of flipping other dipoles
        calc_probs_examples(board)
        board.commit_and_propagate_staged_writes()

    board.history_manager.export_to_file()





# Assuming your JSON data is stored in 'board_data.json'
data = load_json('exampleData.json')
process_board_data(data)
