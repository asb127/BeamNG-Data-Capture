from typing import List, Tuple
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.scenario.scenario_object import ScenarioObject

import logging_mgr, simulation_mgr, vehicle_mgr, utils
from session_config import SessionConfig

# Global variable to store the available weather presets
weather_presets: List[str] = []

# Global variable to store the available waypoints in the scenario
scenario_waypoints: List[ScenarioObject] = []

def teleport_vehicle_to_waypoint(bng: BeamNGpy,
                                 scenario: Scenario,
                                 vehicle: Vehicle,
                                 waypoint: str) -> None:
    '''
    Teleport the vehicle to the provided waypoint in the scenario.

    The waypoint must be a valid waypoint in the scenario.
    Scenario must be loaded, otherwise an error will be triggered.
    '''
    # Scenario must be loaded in the simulator to find waypoints (get_current() doesn't match the scenario)
    if bng.scenario.get_current(False).name != scenario.name:
        logging_mgr.log_error(f'Scenario {scenario} must be loaded in the simulator to use waypoints.')
    else:
        # Check if waypoints have been found in the scenario
        if not scenario_waypoints:
            logging_mgr.log_warning('No waypoints found in the scenario. Cannot teleport vehicle to waypoint.')
        else:
            # Find the waypoint with the provided name
            target_waypoint = next((waypoint_obj for waypoint_obj in scenario_waypoints if waypoint_obj.name == waypoint), None)
            # If the waypoint is found, teleport the vehicle to its position and rotation
            if target_waypoint:
                vehicle_mgr.teleport_vehicle(vehicle,
                                             target_waypoint.pos,
                                              target_waypoint.rot)
                logging_mgr.log_action(f'Vehicle {vehicle.vid} teleported to waypoint "{waypoint}".')
            else:
                logging_mgr.log_warning(f'Waypoint "{waypoint}" not found in the scenario. Vehicle not teleported.')

def teleport_vehicle_to_random_waypoint(bng: BeamNGpy,
                                        scenario: Scenario,
                                        vehicle: Vehicle) -> None:
    '''Teleport the vehicle to a random waypoint in the scenario.'''
    # Retrieve the list of waypoints in the scenario
    waypoints_list = find_waypoints(scenario)
    # If no waypoints are found, log a warning and skip teleporting the vehicle
    if not waypoints_list:
        logging_mgr.log_warning('No waypoints found in the scenario. Skipping vehicle teleportation.')
    else:
        # Select a random waypoint from the list
        waypoint = utils.select_random_item(waypoints_list)
        # Teleport the vehicle to the selected waypoint
        teleport_vehicle_to_waypoint(bng,
                                     scenario,
                                     vehicle,
                                     waypoint)


def find_waypoints(scenario: Scenario) -> List[str]:
    '''Find all waypoints in the scenario and return them in a list of its names.'''
    # Use global list to store the waypoints
    global scenario_waypoints
    scenario_waypoints = scenario.find_waypoints()
    logging_mgr.log_action(f'Found {len(scenario_waypoints)} waypoints in the scenario.')
    # Return the names of the waypoints found
    return [waypoint.name for waypoint in scenario_waypoints]

def create_scenario(bng: BeamNGpy, session: SessionConfig) -> Tuple[Scenario, Vehicle]:
    '''Create a scenario based on the provided session configuration.'''
    # Create a scenario in the given map
    scenario = Scenario(session.map, session.scenario)
    logging_mgr.log_action(f'Scenario "{session.scenario}" created in map "{session.map}".')
    # Create an "ego vehicle" to capture data from
    ego = vehicle_mgr.add_vehicle(scenario,
                                  session.vehicle.name,
                                  session.vehicle.model,
                                  session.vehicle.initial_position,
                                  session.vehicle.initial_rotation)
    # Place files defining the scenario for the simulator to read
    scenario.make(bng)
    logging_mgr.log_action(f'Scenario "{session.scenario}" files created.')
    # Return the created scenario and the "ego" vehicle
    return scenario, ego

def initialize_scenario(bng: BeamNGpy,
                        scenario: Scenario,
                        ego_vehicle: Vehicle,
                        session_config: SessionConfig) -> None:
    '''
    Initialize the scenario in the simulator with the given ego vehicle.
    Also sets the specified weather and number of AI traffic vehicles.
    '''
    # Load and start the scenario in the simulator
    simulation_mgr.load_scenario(bng, scenario)
    simulation_mgr.start_scenario(bng)
    # Set the vehicle AI mode to realistic traffic simulation
    vehicle_mgr.set_vehicle_ai_mode(ego_vehicle,
                                    'traffic',
                                    True)
    # Enable traffic in the scenario with the specified number of vehicles
    simulation_mgr.enable_traffic(bng, session_config.num_ai_traffic_vehicles)
    # Randomize the 'ego' vehicle's color
    vehicle_mgr.randomize_vehicle_color(ego_vehicle)
    # Set weather preset for the scenario
    set_weather_preset(bng, session_config.weather)

def get_weather_presets() -> None:
    '''Load the available weather presets from the settings file into the global variable "weather_presets".'''
    global weather_presets
    import settings
    # Load the weather presets from the path specified in the settings
    weather_presets = utils.load_json_file(settings.weather_presets_path).keys()
    # Log a warning if no weather presets are found
    if weather_presets:
        logging_mgr.log_action(f'Weather presets loaded: {list(weather_presets)}.')
    else:
        logging_mgr.log_warning('No weather presets file found. Weather presets will not be available.')

def set_weather_preset(bng: BeamNGpy, weather_preset: str, transition_time: float = 1) -> None:
    '''
    Set the weather preset for the simulator to the provided preset.

    A transition time can be specified to smooth the weather change.
    '''
    # If no weather preset is provided, skip
    if not weather_preset:
        logging_mgr.log_action('No weather preset provided. Skipping weather preset configuration.')
    # If the weather preset is not available, log a warning
    elif weather_preset not in weather_presets:
        logging_mgr.log_warning(f'Weather preset "{weather_preset}" not available.')
    # Otherwise, proceed with setting the weather preset
    else:
        bng.set_weather_preset(weather_preset, transition_time)
        logging_mgr.log_action(f'Set weather preset to {weather_preset}.')