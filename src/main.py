import data_capture_mgr, simulation_mgr, scenario_mgr, logging_mgr

# Create an output directory to store the session data
output_dir = data_capture_mgr.create_output_dir()

# Set up logging for the data capture process
logging_mgr.configure_logging(output_dir)

# Create BeamNGpy instance and connect to the simulator
bng = simulation_mgr.launch_beamng('localhost', 25252)
logging_msg = 'BeamNGpy instance created and connected to the simulator.'
logging_mgr.log_action(logging_msg)

# Set simulation steps per second to 60
simulation_mgr.set_simulation_steps_per_second(bng, 60)

# Create a scenario and vehicle for the capture session
scenario, ego = scenario_mgr.create_scenario(bng,
                                             'west_coast_usa',
                                             'capture_scenario',
                                             'ego',
                                             'etk800',
                                             (-720, 100, 119),
                                             (0, 0, 0.35, 0.90))

# Initialize the scenario in the simulator
scenario_mgr.initialize_scenario(bng,
                                 scenario,
                                 ego)

# Create camera sensors and attach them to the vehicle
sensor_camera = data_capture_mgr.create_camera_sensor(bng,
                                                      ego,
                                                      'sensor_camera',
                                                      (0, -0.5, 1.5),
                                                      (1280, 720),
                                                      True,
                                                      True,
                                                      True)

try:
    # Capture 10 images, one every 10 seconds
    num_frames = 10
    wait_seconds = 10

    # Iterate to capture one frame
    for i in range(num_frames):
        # Pause the simulation
        simulation_mgr.pause_simulation(bng)
        # Advance the simulation by the corresponding number of seconds
        simulation_mgr.step_simulation_seconds(bng, wait_seconds)
        try:
            # Resume the simulation
            bng.resume()
        except ConnectionResetError:
            # Unable to reconnect with simulation
            logging_msg = 'Connection to simulator reset. Stopping script.'
            logging_mgr.log_error(logging_msg)
            break

        frame_dir = data_capture_mgr.create_frame_output_dir(output_dir, i)
        data_capture_mgr.save_camera_data(sensor_camera, frame_dir)
        simulation_mgr.display_message(bng, f'Frame {i} captured')
except KeyboardInterrupt:
    # User stopped the simulation process
    logging_mgr.log_action('Simulation stopped by user.')
except Exception as e:
    # An unexpected error stopped the simulation process
    logging_mgr.log_error(f'Simulation stopped by an unexpected error: {e}')
finally:
    # Simulation finished, close
    logging_mgr.log_action('Simulation finished.')
    simulation_mgr.close_beamng(bng)
