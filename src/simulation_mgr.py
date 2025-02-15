from beamngpy import BeamNGpy

def launch_beamng(host, port):
    # Instantiate BeamNGpy instance connecting to the simulator on the given host and port
    bng = BeamNGpy(host, port)
    # Launch the simulator
    bng.open()
    return bng

def set_simulation_steps_per_second(bng, steps_per_second):
    # Store the value of the simulation steps per second in a global variable
    global simulation_steps_per_second
    simulation_steps_per_second = steps_per_second
    # Set simulation steps per second to the given value
    bng.set_steps_per_second(steps_per_second)

def load_scenario(bng, scenario):
    # Load the given scenario in the simulator
    bng.load_scenario(scenario)

def start_scenario(bng):
    # Start the scenario in the simulator
    bng.start_scenario()

def set_vehicle_ai_mode(vehicle, mode, in_lane):
    # Set the vehicle's AI mode and lane driving behavior
    vehicle.ai.set_mode(mode)
    vehicle.ai.drive_in_lane(in_lane)

def enable_traffic(bng, max_amount):
    # Enable or disable AI traffic in the scenario
    bng.traffic.spawn(max_amount=max_amount)
