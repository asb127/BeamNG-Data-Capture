import os, logging
from datetime import datetime

log_file = ''

def configure_logging(output_dir):
    """Set up the logging module to output the log messages into a file."""
    # Create a file to store the log messages
    log_file = os.path.join(output_dir, 'log.txt')
    # Configure the logging module
    logging.basicConfig(filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(message):
    """Write an error message in the log file."""
    logging.error(message)

def log_action(message):
    """Write an action message in the log file."""
    logging.info(message)
