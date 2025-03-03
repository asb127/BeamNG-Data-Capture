from beamngpy import BeamNGpy
from beamngpy.vehicle import Vehicle
from beamngpy.scenario import Scenario

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
    # Advance the simulation by the given number of steps
    bng.step(steps)

def step_simulation_seconds(bng: BeamNGpy, seconds: int) -> None:
    # Advance the simulation the corresponding number of steps for the given number of seconds
    steps = int(seconds * simulation_steps_per_second)
    bng.step(steps)
    logging_mgr.log_action(f'Simulation advanced by {seconds} seconds.')

def set_simulation_steps_per_second(bng: BeamNGpy, steps_per_second: int) -> None:
    # Store the value of the simulation steps per second in the global variable
    global simulation_steps_per_second
    simulation_steps_per_second = steps_per_second
    # Set simulation steps per second to the given value
    bng.set_steps_per_second(simulation_steps_per_second)

def load_scenario(bng: BeamNGpy, scenario: Scenario) -> None:
    # Load the given scenario in the simulator
    bng.load_scenario(scenario)

def start_scenario(bng: BeamNGpy) -> None:
    # Start the scenario in the simulator
    bng.start_scenario()

def set_vehicle_ai_mode(vehicle: Vehicle,
                        mode: str,
                        in_lane: bool) -> None:
    # Set the vehicle's AI mode and lane driving behavior
    vehicle.ai.set_mode(mode)
    vehicle.ai.drive_in_lane(in_lane)
    logging_mgr.log_action(f'Set AI mode to {mode} and in-lane driving to {in_lane}.')

def enable_traffic(bng: BeamNGpy, max_traffic_amount: int) -> None:
    # Enable or disable AI traffic in the scenario
    bng.traffic.spawn(max_amount=max_traffic_amount)
    logging_mgr.log_action(f'Enabling AI traffic with a maximum of {max_traffic_amount} vehicles.')

def display_message(bng: BeamNGpy, message: str) -> None:
    # Display a message on the simulator's UI
    bng.ui.display_message(message)
    logging_mgr.log_action(message)
