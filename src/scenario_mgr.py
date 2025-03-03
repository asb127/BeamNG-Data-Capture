import random
from beamngpy import BeamNGpy, Scenario, Vehicle

import simulation_mgr, logging_mgr
from session_config import SessionConfig

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
                        ego_vehicle: Vehicle) -> None:
    # Load and start the scenario in the simulator
    simulation_mgr.load_scenario(bng, scenario)
    simulation_mgr.start_scenario(bng)
    # Set the vehicle AI mode to realistic traffic simulation
    set_vehicle_ai_mode(ego_vehicle,
                        'traffic',
                        True)
    # Enable traffic in the scenario with a maximum of 10 vehicles
    simulation_mgr.enable_traffic(bng, 10)
    # Randomize the 'ego' vehicle's color
    randomize_vehicle_color(ego_vehicle)

def set_vehicle_ai_mode(vehicle: Vehicle,
                        mode: str,
                        in_lane: bool) -> None:
    # Set the vehicle's AI mode and lane driving behavior
    vehicle.ai.set_mode(mode)
    vehicle.ai.drive_in_lane(in_lane)
