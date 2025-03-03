import random
from typing import List
from beamngpy import BeamNGpy, Scenario, Vehicle

import simulation_mgr, logging_mgr, settings, utils
from session_config import SessionConfig

# Global variable to store the available weather presets
weather_presets: List[str] = []

def randomize_vehicle_color(vehicle: Vehicle) -> None:
    vehicle.set_color((random.uniform(0, 1),
                       random.uniform(0, 1),
                       random.uniform(0, 1),
                       random.uniform(0, 1)))

def add_vehicle(scenario: Scenario,
                vehicle_name: str,
                model: str,
                pos: tuple,
                rot_quat: tuple) -> Vehicle:
    # Create a vehicle with the provided name and model
    vehicle = Vehicle(vehicle_name, model=model)
    logging_mgr.log_action(f'Vehicle created: "{vehicle_name}" (model "{model}").')
    # Add the vehicle to the scenario, with the specified position and rotation
    scenario.add_vehicle(vehicle,
                         pos=pos,
                         rot_quat=rot_quat)
    logging_mgr.log_action(f'Vehicle {vehicle_name} added to the scenario in position {pos} with rotation {rot_quat}.')
    # Return the created vehicle
    return vehicle

def create_scenario(bng: BeamNGpy, session: SessionConfig) -> tuple:
    # Create a scenario in the given map
    scenario = Scenario(session.map, session.scenario)
    logging_mgr.log_action(f'Scenario "{session.scenario}" created in map "{session.map}".')
    # Create an "ego vehicle" to capture data from
    ego = add_vehicle(scenario,
                      session.vehicle.name,
                      session.vehicle.model,
                      session.vehicle.initial_position,
                      session.vehicle.initial_rotation)
    logging_mgr.log_action(f'Ego vehicle "{session.vehicle.name}" added to scenario.')
    # Place files defining the scenario for the simulator to read
    scenario.make(bng)
    logging_mgr.log_action(f'Scenario "{session.scenario}" files created.')
    # Return the created scenario and the "ego" vehicle
    return scenario, ego

def initialize_scenario(bng: BeamNGpy,
                        scenario: Scenario,
                        ego_vehicle: Vehicle,
                        session_config: SessionConfig) -> None:
    # Load and start the scenario in the simulator
    simulation_mgr.load_scenario(bng, scenario)
    simulation_mgr.start_scenario(bng)
    # Set the vehicle AI mode to realistic traffic simulation
    set_vehicle_ai_mode(ego_vehicle,
                        'traffic',
                        True)
    # Enable traffic in the scenario with the specified number of vehicles
    simulation_mgr.enable_traffic(bng, session_config.num_ai_traffic_vehicles)
    # Randomize the 'ego' vehicle's color
    randomize_vehicle_color(ego_vehicle)
    # Set weather preset for the scenario
    set_weather_preset(bng, session_config.weather)

def set_vehicle_ai_mode(vehicle: Vehicle,
                        mode: str,
                        in_lane: bool) -> None:
    # Set the vehicle's AI mode and lane driving behavior
    vehicle.ai.set_mode(mode)
    vehicle.ai.drive_in_lane(in_lane)

def get_weather_presets() -> None:
    # Store the available weather presets into the global variable 'weather_presets'
    global weather_presets
    # Load the weather presets from the path specified in the settings
    weather_presets = utils.load_json_file(settings.weather_presets_path).keys()
    # Log a warning if no weather presets are found
    if weather_presets:
        logging_mgr.log_action(f'Weather presets loaded: {list(weather_presets)}.')
    else:
        logging_mgr.log_warning('No weather presets file found. Weather presets will not be available.')

def set_weather_preset(bng: BeamNGpy, weather_preset: str, time: float = 1) -> None:
    # Set the provided weather preset in the simulator
    # If no weather preset is provided, skip
    if not weather_preset:
        logging_mgr.log_action('No weather preset provided. Skipping weather preset configuration.')
    # If the weather preset is not available, log a warning
    elif weather_preset not in weather_presets:
        logging_mgr.log_warning(f'Weather preset "{weather_preset}" not available.')
    else:
        bng.set_weather_preset(weather_preset, time)
        logging_mgr.log_action(f'Set weather preset to {weather_preset}.')