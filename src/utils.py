import os
from datetime import datetime

import logging_mgr

def return_documents_path() -> str:
    # Return the path to the user's "Documents" folder
    return os.path.expanduser('~/Documents')

def create_output_dir(root_dir: str) -> str:
    # Create a directory to store the captured images
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = os.path.join(root_dir,
                              'BeamNG-Data-Capture',
                              timestamp)
    os.makedirs(output_dir, exist_ok=True)
    logging_mgr.log_action(f'Output directory created at {output_dir}.')
    return output_dir

def create_frame_output_dir(output_dir: str, i: int) -> str:
    # Create a subfolder for every frame
    frame_dir = os.path.join(output_dir, f'frame_{i}')
    os.makedirs(frame_dir, exist_ok=True)
    logging_mgr.log_action(f'Frame {i} output directory created at {output_dir}.')
    return frame_dir

