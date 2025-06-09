import json, os, random, re, zipfile
from datetime import datetime
from typing import List
from scipy.spatial.transform import Rotation as R
from beamngpy.types import Quat

import gui_mgr, logging_mgr

# --- Time/Date Utilities ---
def get_time() -> int:
    '''
    Return the current time as an integer POSIX timestamp.
    '''
    return int(datetime.now().timestamp())

def is_hhmmss_time_string(time_str: str) -> bool:
    '''
    Check if the string is in BeamNG time format (HH:mm:ss).
    '''
    # Regex: HH:mm:ss where HH is 00-23 and both mm and ss are 00-59
    pattern = r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$'
    return bool(re.match(pattern, time_str))

def beamng_time_to_hhmmss(time: float) -> str:
    '''
    Convert BeamNG time [0,1] to HH:mm:ss format.
    Note: Both 0 and 1 in BeamNG time are 12:00:00.
    '''
    # Convert BeamNG time to seconds (1 day = 86400 seconds)
    seconds = time * 86400
    # Adjust the time to start at 00:00:00
    seconds += 43200
    # If the time is greater than 24 hours, subtract 24 hours
    seconds %= 86400
    # Convert seconds to hours, minutes, and seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    # Return the time as a string in HH:mm:ss format
    return f'{hours:02}:{minutes:02}:{seconds:02}'

def hhmmss_to_beamng_time(time: str) -> float:
    '''
    Convert HH:mm:ss format to BeamNG time [0,1].
    Note: Both 0 and 1 in BeamNG time are 12:00:00.
    '''
    return_time = 0.0
    if not is_hhmmss_time_string(time):
        logging_mgr.log_error('Invalid time format. Must be in HH:mm:ss format.')
        raise ValueError('Invalid time format. Must be in HH:mm:ss format.')
    else:
        hours, minutes, seconds = map(int, time.split(':'))
        total_seconds = hours * 3600 + minutes * 60 + seconds
        total_seconds -= 43200
        total_seconds %= 86400
        return_time = total_seconds / 86400
    return return_time

# --- Path/File Utilities ---
def return_documents_path() -> str:
    '''
    Return the path to the user's "Documents" folder.
    '''
    return os.path.expanduser('~/Documents')

def join_paths(*args) -> str:
    '''
    Join non-empty string arguments into a single path.
    '''
    accepted_args = accept_string_args(*args)
    return os.path.join(*accepted_args)

def create_dir(path: str, name: str) -> str:
    '''
    Create a directory with the given name at the specified path.
    Return the full path to the created directory.
    '''
    dir_path = os.path.join(path, name)
    os.makedirs(dir_path, exist_ok=True)
    logging_mgr.log_action(f'Directory created at "{dir_path}".')
    return dir_path

def create_output_dir(root_dir: str) -> str:
    '''
    Create a directory to store the captured images.
    The directory is named with the current timestamp.
    '''
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return create_dir(root_dir, os.path.join('BeamNG-Data-Capture', timestamp))

def create_frame_output_dir(output_dir: str, i: int) -> str:
    '''
    Create a subfolder for every frame inside the output directory.
    '''
    return create_dir(output_dir, f'frame_{i}')

# --- Random Utilities ---
def set_random_seed(seed: int) -> None:
    '''
    Set the random seed for reproducibility.
    '''
    random.seed(seed)
    logging_mgr.log_action(f'Random seed set to {seed}.')

def get_random_float(min_value: float, max_value: float) -> float:
    '''
    Generate a random float between the specified minimum and maximum values.
    '''
    return random.uniform(min_value, max_value)

def select_random_item(items: List) -> object:
    '''
    Select a random item from the provided list.
    '''
    return random.choice(items)

# --- Data Structure Utilities ---
def accept_string_args(*args) -> List[str]:
    '''
    Only accept non-empty string arguments from the provided arguments.
    '''
    accepted_args: List[str] = []
    for arg in args:
        if not isinstance(arg, str):
            logging_mgr.log_warning(f'Argument is not a string: "{arg}".')
        elif not arg:
            logging_mgr.log_warning(f'Empty string argument detected.')
        else:
            accepted_args.append(arg)
    return accepted_args

def combine_dict(metadata_array: List[dict]) -> dict:
    '''
    Combine all metadata dictionaries in the list into a single dictionary.
    '''
    combined_metadata = {}
    for metadata in metadata_array:
        combined_metadata.update(metadata)
    logging_mgr.log_action(f'Dictionary array combined with keys: {list(combined_metadata.keys())}.')
    return combined_metadata

def create_parent_dict(keys: List[str], values: List[dict]) -> dict:
    '''
    Create a dictionary with the provided strings as keys and dictionaries as values.
    '''
    output_dict = dict()
    if len(keys) != len(values):
        logging_mgr.log_error('Could not create parent dictionary: keys and values lists must have the same length.')
        raise ValueError('Could not create parent dictionary: keys and values lists must have the same length.')
    else:
        output_dict = dict(zip(keys, values))
        logging_mgr.log_action(f'Dictionary created with keys: {list(output_dict.keys())}.')
    return output_dict

def create_child_dict(parent_dict:dict, key: str) -> dict:
    '''
    Create a child dictionary with the provided key from the parent dictionary.
    '''
    child_dict = parent_dict.get(key, dict())
    # If the key does not exist, log a warning
    if not child_dict:
        logging_mgr.log_warning(f'Child dictionary not found with key "{key}".')
    else:
        logging_mgr.log_action(f'Child dictionary created with key "{key}".')
    return child_dict

# --- JSON/ZIP Utilities ---
def save_json_file(data: dict, output_dir: str, filename: str) -> None:
    '''
    Save the provided data as a JSON file in the output directory.
    '''
    with open(os.path.join(output_dir, filename), 'w') as file:
        json.dump(data, file, indent=4)
    logging_mgr.log_action(f'JSON file "{filename}" saved in "{output_dir}".')

def is_path_inside_zip(path: str) -> bool:
    '''
    Check if the provided path is contained within a ZIP file.
    '''
    return '.zip/' in path

def load_json_file(file_path: str) -> dict:
    '''
    Load a JSON file from the provided path.
    If the path is inside a ZIP file, extract and load it.
    '''
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
    '''
    Open the provided ZIP file and return the ZipFile object.
    '''
    zip_file = zipfile.ZipFile(file_path, 'r')
    logging_mgr.log_action(f'ZIP file "{file_path}" opened.')
    return zip_file

def read_file_inside_zip(zip_file: zipfile.ZipFile, file_path: str) -> str:
    '''
    Read the provided file inside the ZIP file and return its contents as bytes.
    '''
    with zip_file.open(file_path) as file:
        data = file.read()
    logging_mgr.log_action(f'File "{file_path}" read inside ZIP file.')
    return data

def read_json_file_inside_zip(zip_file: zipfile.ZipFile, file_path: str) -> dict:
    '''
    Read the provided JSON file inside the ZIP file and return its contents as a dictionary.
    '''
    data = read_file_inside_zip(zip_file, file_path)
    # Decode the data into a dictionary
    dictionary = json.loads(data.decode('utf-8'))
    logging_mgr.log_action(f'JSON file "{file_path}" read inside ZIP file.')
    return dictionary

# --- Logging/GUI Helpers ---
def log_and_show_error(message: str) -> None:
    '''
    Log an error and show it to the user via GUI.
    '''
    logging_mgr.log_error(message)
    gui_mgr.show_error_message(message)

def euler_to_quaternion(roll: float, pitch: float, yaw: float, degrees: bool = True) -> Quat:
    '''
    Convert Euler angles to a quaternion (qx, qy, qz, qw).
    By default, assumes input is in degrees unless degrees=False (uses radians instead).
    '''
    r = R.from_euler('xyz', [roll, pitch, yaw], degrees=degrees)
    qx, qy, qz, qw = r.as_quat()
    return Quat(qx, qy, qz, qw)

def tuple_from_str(s: str, type_cast, expected_len: int, sep: str = ",") -> tuple:
    '''
    Split a string (e.g. "1, 2, 3") into a tuple of type_casted values.
    Raises ValueError if the number of elements does not match expected_len.
    '''
    parts = [type_cast(x.strip()) for x in s.split(sep)]
    if len(parts) != expected_len:
        raise ValueError(f"Expected {expected_len} values, got {len(parts)}: '{s}'")
    return tuple(parts)
