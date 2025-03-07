import json, os, random, zipfile
from datetime import datetime
from typing import List

import logging_mgr

def get_time() -> int:
    # Return the current time as an integer
    return int(datetime.now().timestamp())

def set_random_seed(seed: int) -> None:
    # Set the random seed for reproducibility
    random.seed(seed)
    logging_mgr.log_action(f'Random seed set to {seed}.')

def get_random_float(min_value: float, max_value: float) -> float:
    # Generate a random float between the specified minimum and maximum values
    return random.uniform(min_value, max_value)

def select_random_item(items: List) -> object:
    # Select a random item from the provided list
    return random.choice(items)

def accept_string_args(*args) -> List[str]:
    # Only accept non-empty string arguments
    accepted_args: List[str] = []
    for arg in args:
        if not isinstance(arg, str):
            logging_mgr.log_warning(f'Argument is not a string: "{arg}".')
        elif not arg:
            logging_mgr.log_warning(f'Empty string argument detected.')
        else:
            accepted_args.append(arg)
    return accepted_args

def return_documents_path() -> str:
    # Return the path to the user's "Documents" folder
    return os.path.expanduser('~/Documents')

def join_paths(*args) -> str:
    # Join non-empty string arguments into a single path
    accepted_args = accept_string_args(*args)
    return os.path.join(*accepted_args)

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

def combine_dict(metadata_array: List[dict]) -> dict:
    # Combine all metadata into a single dictionary
    combined_metadata = {}
    for metadata in metadata_array:
        combined_metadata.update(metadata)
    logging_mgr.log_action(f'Dictionary array combined with keys: {list(combined_metadata.keys())}.')
    return combined_metadata

def create_parent_dict(keys: List[str], values: List[dict]) -> dict:
    # Create a dictionary with the provided strings as keys and dictionaries as values
    output_dict = dict()
    if len(keys) != len(values):
        logging_mgr.log_error('Could not create parent dictionary: keys and values lists must have the same length.')
    else:
        output_dict = dict(zip(keys, values))
        logging_mgr.log_action(f'Dictionary created with keys: {list(output_dict.keys())}.')
    return output_dict

def create_child_dict(parent_dict:dict, key: str) -> dict:
    # Create a child dictionary with the provided key from the parent dictionary
    child_dict = parent_dict.get(key, dict())
    # If the key does not exist, log a warning
    if not child_dict:
        logging_mgr.log_warning(f'Child dictionary not found with key "{key}".')
    else:
        logging_mgr.log_action(f'Child dictionary created with key "{key}".')
    return child_dict

def save_json_file(data: dict, output_dir: str, filename: str) -> None:
    # Save the provided data as a JSON file in the output directory
    with open(os.path.join(output_dir, filename), 'w') as file:
        json.dump(data, file, indent=4)
    logging_mgr.log_action(f'JSON file "{filename}" saved in "{output_dir}".')

def is_path_inside_zip(path: str) -> bool:
    # Check if the provided path is contained within a ZIP file
    return '.zip/' in path

def load_json_file(file_path: str) -> dict:
    # Check if the provided path is inside a ZIP file
    if is_path_inside_zip(file_path):
        # Split the path into the ZIP file and the file inside it
        zip_path, file_inside_zip = file_path.split('.zip', 1)
        # Preserve the '.zip' extension in the ZIP file path
        zip_path += '.zip'
        # Remove the leading slash from the file inside the ZIP
        file_inside_zip = file_inside_zip[1:]
        # Open the ZIP file and read the JSON file inside, storing the data in an output dictionary
        with open_zip_file(zip_path) as zip_file:
            data = read_json_file_inside_zip(zip_file, file_inside_zip)
    else:
        # Load a JSON file from the provided path into an output dictionary
        with open(file_path, 'r') as file:
            data = json.load(file)
            logging_mgr.log_action(f'JSON file "{file_path}" loaded.')
    return data

def open_zip_file(file_path: str) -> zipfile.ZipFile:
    # Open the provided ZIP file
    zip_file = zipfile.ZipFile(file_path, 'r')
    logging_mgr.log_action(f'ZIP file "{file_path}" opened.')
    return zip_file

def read_file_inside_zip(zip_file: zipfile.ZipFile, file_path: str) -> str:
    # Read the provided file inside the ZIP file
    with zip_file.open(file_path) as file:
        data = file.read()
    logging_mgr.log_action(f'File "{file_path}" read inside ZIP file.')
    return data

def read_json_file_inside_zip(zip_file: zipfile.ZipFile, file_path: str) -> dict:
    # Read the provided JSON file inside the ZIP file
    data = read_file_inside_zip(zip_file, file_path)
    # Decode the data into a dictionary
    dictionary = json.loads(data)
    logging_mgr.log_action(f'JSON file "{file_path}" read inside ZIP file.')
    return dictionary