from beamngpy import BeamNGpy

import logging_mgr

# Global variable to store the simulation steps per second
simulation_steps_per_second = 0

def launch_beamng(host, port):
    # Instantiate BeamNGpy instance connecting to the simulator on the given host and port
    bng = BeamNGpy(host, port)
    logging_mgr.log_action(f'BeamNGpy instance {bng} created.')
    # Launch the simulator
    bng.open()
    logging_mgr.log_action(f'BeamNGpy instance {bng} connected to the simulator.')
    return bng

def close_beamng(bng):
    # Close the simulator
    bng.close()
    logging_mgr.log_action(f'BeamNGpy instance {bng} closed.')

def pause_simulation(bng):
    # Pause the simulation
    bng.pause()
    logging_mgr.log_action('Simulation paused.')

def resume_simulation(bng):
    # Resume the simulation
    bng.resume()
    logging_mgr.log_action('Simulation resumed.')

def step_simulation_steps(bng, steps):
    # Advance the simulation by the given number of steps
    bng.step(steps)
    logging_mgr.log_action(f'Simulation advanced by {steps} steps.')

def step_simulation_seconds(bng, seconds):
    # Advance the simulation the corresponding number of steps for the given number of seconds
    steps = seconds * simulation_steps_per_second
    bng.step(steps)
    logging_mgr.log_action(f'Simulation advanced by {seconds} seconds ({steps} steps).')

def set_simulation_steps_per_second(bng, steps_per_second):
    # Store the value of the simulation steps per second in the global variable
    global simulation_steps_per_second
    simulation_steps_per_second = steps_per_second
    # Set simulation steps per second to the given value
    bng.set_steps_per_second(simulation_steps_per_second)
    logging_mgr.log_action(f'Simulation steps per second set to {simulation_steps_per_second}.')

def load_scenario(bng, scenario):
    # Load the given scenario in the simulator
    bng.load_scenario(scenario)
    logging_mgr.log_action(f'Scenario {scenario} loaded.')

def start_scenario(bng):
    # Start the scenario in the simulator
    bng.start_scenario()
    logging_mgr.log_action('Scenario started.')

def set_vehicle_ai_mode(vehicle, mode, in_lane):
    # Set the vehicle's AI mode and lane driving behavior
    vehicle.ai.set_mode(mode)
    vehicle.ai.drive_in_lane(in_lane)
    logging_mgr.log_action(f'Set AI mode to {mode} and in-lane driving to {in_lane}.')

def enable_traffic(bng, max_traffic_amount):
    # Enable or disable AI traffic in the scenario
    bng.traffic.spawn(max_amount=max_traffic_amount)
    logging_mgr.log_action(f'Enabling AI traffic with a maximum of {max_traffic_amount} vehicles.')

def display_message(bng, message):
    # Display a message on the simulator's UI
    bng.ui.display_message(message)
    logging_mgr.log_action(message)
