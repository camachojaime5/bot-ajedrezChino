import json

DEFAULT_DIRECTORY = 'data/'
DEFAULT_OUTPUT = 'output.json'
DEFAULT_INPUT = 'input.json'

def input_json(file_name = None):
    if not file_name:
        file_name = DEFAULT_INPUT
    with open(DEFAULT_DIRECTORY + file_name, "r") as file:
        return json.load(file)


def output_json(state, output_name = None):
    if not output_name:
        output_name = DEFAULT_OUTPUT
    with open(DEFAULT_DIRECTORY + output_name, "w") as file:
        json.dump(state, file)