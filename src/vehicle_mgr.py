from beamngpy import Scenario, Vehicle
from type_defs import Float3, Quat

import logging_mgr, utils

def randomize_vehicle_color(vehicle: Vehicle) -> None:
    """Sets the color of the vehicle to a random RGBA color."""
    vehicle.set_color((utils.get_random_float(0, 1),
                       utils.get_random_float(0, 1),
                       utils.get_random_float(0, 1),
                       utils.get_random_float(0, 1)))

def add_vehicle(scenario: Scenario,
                vehicle_name: str,
                model: str,
                pos: Float3,
                rot_quat: Quat) -> Vehicle:
    """Add a vehicle to the scenario with the provided name, model, position and rotation."""
    # Create a vehicle with the provided name and model
    vehicle = Vehicle(vehicle_name, model=model)
    logging_mgr.log_action(f'Vehicle created: "{vehicle_name}" (model "{model}").')
    # Add the vehicle to the scenario, with the specified position and rotation
    scenario.add_vehicle(vehicle,
                         pos,
                         rot_quat)
    logging_mgr.log_action(f'Vehicle {vehicle_name} added to the scenario in position {pos} with rotation {rot_quat}.')
    # Return the created vehicle
    return vehicle

def teleport_vehicle(vehicle: Vehicle,
                     pos: Float3,
                     rot_quat: Quat) -> None:
    """Teleport the vehicle to the provided position and rotation."""
    vehicle.teleport(pos, rot_quat)
    logging_mgr.log_action(f'Vehicle {vehicle.vid} teleported to position {pos} with rotation {rot_quat}.')


def set_vehicle_ai_mode(vehicle: Vehicle,
                        mode: str,
                        in_lane: bool) -> None:
    """Set the vehicle's AI mode and lane driving behavior to the provided values."""
    vehicle.ai.set_mode(mode)
    vehicle.ai.drive_in_lane(in_lane)
    logging_mgr.log_action(f'Set AI mode to {mode} and in-lane driving to {in_lane}.')

def set_headlights(vehicle: Vehicle, intensity: int) -> None:
    """
    Set the intensity of the vehicle's headlights.
    
    For intensity: 0 is off, 1 is low, 2 is high, any other value is ignored.
    """
    if intensity not in [0, 1, 2]:
        logging_mgr.log_warning(f'Invalid intensity value {intensity} for vehicle headlights.')
    else:
        vehicle.set_lights(headlights=intensity)
        logging_mgr.log_action(f'Set vehicle headlights intensity to {intensity}.')