from beamngpy import BeamNGpy
from beamngpy.scenario import Scenario
from type_defs import StrDict, Time

import logging_mgr, settings

# Global variable to store the simulation steps per second
simulation_steps_per_second: int = 0

def launch_beamng() -> BeamNGpy:
    # Instantiate BeamNGpy instance connecting to the simulator
    # Uses the specified settings for host, port and home path
    bng = BeamNGpy(settings.beamng_host, settings.beamng_port, settings.beamng_home_path)
    # Launch the simulator
    bng.open()
    return bng

def close_beamng(bng: BeamNGpy) -> None:
    # Close the simulator
    bng.close()

def pause_simulation(bng: BeamNGpy) -> None:
    # Pause the simulation
    bng.pause()

def resume_simulation(bng: BeamNGpy) -> None:
    # Resume the simulation
    bng.resume()

def step_simulation_steps(bng: BeamNGpy, steps: int) -> None:
    # Advance the simulation by the given number of steps (if larger than 0)
    if (steps > 0):
        bng.step(steps)
    else:
        logging_mgr.log_warning(f'Requested steps ignored, value must be higher than zero. Value requested: {steps}.')

def step_simulation_seconds(bng: BeamNGpy, seconds: int) -> None:
    # Advance the simulation the corresponding number of steps for the given number of seconds
    steps = int(seconds * simulation_steps_per_second)
    step_simulation_steps(bng, steps)
    logging_mgr.log_action(f'Simulation advanced by {seconds} seconds.')

def set_deterministic_steps_per_second(bng: BeamNGpy, steps_per_second: int) -> None:
    # Store the value of the deterministic steps per second in the global variable
    global simulation_steps_per_second
    simulation_steps_per_second = steps_per_second
    # Set deterministic mode and simulation steps per second to the given value
    bng.set_deterministic(simulation_steps_per_second)

def load_scenario(bng: BeamNGpy, scenario: Scenario) -> None:
    # Load the given scenario in the simulator
    bng.load_scenario(scenario)

def start_scenario(bng: BeamNGpy) -> None:
    # Start the scenario in the simulator
    bng.start_scenario()

def enable_traffic(bng: BeamNGpy, max_traffic_amount: int) -> None:
    # Enable or disable AI traffic in the scenario
    bng.traffic.spawn(max_amount=max_traffic_amount)
    logging_mgr.log_action(f'Enabling AI traffic with a maximum of {max_traffic_amount} vehicles.')

def get_time_of_day(bng: BeamNGpy) -> StrDict:
    # Get the current time of day in the simulator
    tod = bng.env.get_tod()
    logging_mgr.log_action(f'Simulation time of day retrieved: {tod["time"]}')
    return tod

def set_time_of_day(bng: BeamNGpy,
                    time_of_day: Time | None = None,
                    play: bool | None = None,
                    day_scale: float | None = None,
                    night_scale: float | None = None,
                    day_length: float | None = None) -> None:
    # Set the time of day in the simulator (0.0 to 1.0)
    bng.env.set_tod(tod=time_of_day,
                    play=play,
                    day_scale=day_scale,
                    night_scale=night_scale,
                    day_length=day_length)
    # Log any changes made (values that are not None)
    if time_of_day:
        logging_mgr.log_action(f'Set simulation time of day to {time_of_day}.')
    if type(play) == bool:
        logging_mgr.log_action(f'Set time of day "play" to {play}.')
    if day_scale:
        logging_mgr.log_action(f'Set time of day "day scale" to {day_scale}.')
    if night_scale:
        logging_mgr.log_action(f'Set time of day "night scale" to {night_scale}.')
    if day_length:
        logging_mgr.log_action(f'Set time of day "day length" to {day_length} seconds.')

def display_message(bng: BeamNGpy, message: str) -> None:
    # Display a message on the simulator's UI
    bng.ui.display_message(message)
    logging_mgr.log_action(message)
