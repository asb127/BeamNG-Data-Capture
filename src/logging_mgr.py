import os, logging
import beamngpy.logging as bng_logging

log_file = ''

def configure_logging(output_dir: str) -> None:
    """Set up the logging module to output the log messages into a file."""
    global log_file
    # Create a file to store the log messages
    log_file = os.path.join(output_dir, 'log.txt')
    # Configure the logging module
    bng_logging.set_up_simple_logging(log_file)

def log_error(message: str) -> None:
    """Write an error message in the log file."""
    bng_logging.module_logger.error(message)

def log_action(message: str) -> None:
    """Write an action message in the log file."""
    bng_logging.module_logger.info(message)
