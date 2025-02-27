import os, json
from datetime import datetime

import logging_mgr

def return_documents_path() -> str:
    # Return the path to the user's "Documents" folder
    return os.path.expanduser('~/Documents')

def create_dir(path: str, name: str) -> str:
    # Create a directory with the given name at the specified path
    dir_path = os.path.join(path, name)
    os.makedirs(dir_path, exist_ok=True)
    logging_mgr.log_action(f'Directory created at "{dir_path}".')
    return dir_path

def create_output_dir(root_dir: str) -> str:
    # Create a directory to store the captured images
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return create_dir(root_dir, os.path.join('BeamNG-Data-Capture', timestamp))

def create_frame_output_dir(output_dir: str, i: int) -> str:
    # Create a subfolder for every frame
    return create_dir(output_dir, f'frame_{i}')

def combine_dict(metadata_array: list) -> dict:
    # Combine all metadata into a single dictionary
    combined_metadata = {}
    for metadata in metadata_array:
        combined_metadata.update(metadata)
    logging_mgr.log_action(f'Dictionary array combined with keys: {list(combined_metadata.keys())}.')
    return combined_metadata

def save_json_file(data: dict, output_dir: str, filename: str) -> None:
    # Save the provided data as a JSON file in the output directory
    with open(os.path.join(output_dir, filename), 'w') as file:
        json.dump(data, file, indent=4)
    logging_mgr.log_action(f'JSON file "{filename}" saved in "{output_dir}".')

def load_json_file(file_path: str) -> dict:
    # Load a JSON file from the provided path into an output dictionary
    with open(file_path, 'r') as file:
        data = json.load(file)
    logging_mgr.log_action(f'JSON file "{file_path}" loaded.')
    return data
