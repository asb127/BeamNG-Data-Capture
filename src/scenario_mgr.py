import random
from beamngpy import BeamNGpy, Scenario, Vehicle

import simulation_mgr

def randomize_vehicle_color(vehicle):
    vehicle.set_color((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))

def add_vehicle(scenario, vehicle_name, model, pos, rot_quat):
    # Create a vehicle with the provided name and model
    vehicle = Vehicle(vehicle_name, model=model)
    # Add the vehicle to the scenario, with the specified position and rotation
    scenario.add_vehicle(vehicle, pos=pos, rot_quat=rot_quat)
    # Return the created vehicle
    return vehicle

def create_scenario(bng, map_name, scenario_name, ego_vehicle_name, model, pos, rot_quat):
    # Create a scenario in the given map
    scenario = Scenario(map_name, scenario_name)
    # Create an "ego vehicle" to capture data from
    ego = add_vehicle(scenario, ego_vehicle_name, model, pos, rot_quat)
    # Place files defining the scenario for the simulator to read
    scenario.make(bng)
    # Return the created scenario and the "ego" vehicle
    return scenario, ego

def initialize_scenario(bng, scenario, ego_vehicle):
    # Load and start the scenario in the simulator
    simulation_mgr.load_scenario(bng, scenario)
    simulation_mgr.start_scenario(bng)
    # Set the vehicle AI mode to realistic traffic simulation
    set_vehicle_ai_mode(ego_vehicle, 'traffic', True)
    # Enable traffic in the scenario with a maximum of 10 vehicles
    simulation_mgr.enable_traffic(bng, 10)
    # Randomize the 'ego' vehicle's color
    randomize_vehicle_color(ego_vehicle)


def set_vehicle_ai_mode(vehicle, mode, in_lane):
    # Set the vehicle's AI mode and lane driving behavior
    vehicle.ai.set_mode(mode)
    vehicle.ai.drive_in_lane(in_lane)
