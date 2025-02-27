import data_capture_mgr, simulation_mgr, scenario_mgr, logging_mgr, utils

# Create an output directory to store the session data
root_dir = utils.return_documents_path()
output_dir = utils.create_output_dir(root_dir)

# Set up logging for the data capture process
logging_mgr.configure_logging(output_dir)

# Create BeamNGpy instance and connect to the simulator
bng = simulation_mgr.launch_beamng('localhost', 25252)

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

# Create camera sensor and attach it to the vehicle
sensor_camera = data_capture_mgr.create_camera_sensor(bng,
                                                      ego,
                                                      'sensor_camera',
                                                      (0, -0.5, 1.5),
                                                      (1280, 720),
                                                      True,
                                                      True,
                                                      True)

# Create an IMU sensor and attach it to the vehicle
sensor_imu = data_capture_mgr.create_imu_sensor(bng,
                                                ego,
                                                'sensor_imu')

try:
    # Capture images for 10 seconds, one every 2 seconds
    session_length_s = 10
    capture_freq_hz = 0.5

    capture_period_s = 1 / capture_freq_hz
    num_frames = int(session_length_s * capture_freq_hz)

    logging_mgr.log_action(f'Starting capture session for {session_length_s} seconds with {capture_freq_hz} Hz capture frequency.')
    logging_mgr.log_action(f'Capturing {num_frames} total frames.')

    # Produce error if session length isn't larger than 0
    if session_length_s <= 0:
        raise ValueError('Session length must be a positive number.')
    
    # Produce error if capture frequency isn't larger than 0
    if capture_freq_hz <= 0:
        raise ValueError('Capture frequency must be a positive number.')
    
    # Produce error if capture frequency is larger than simulation steps per second
    if capture_freq_hz > simulation_mgr.simulation_steps_per_second:
        raise ValueError('Capture frequency cannot be larger than simulation steps per second.')
    
    # Produce error if the number of frames is not bigger than 0
    if num_frames <= 0:
        raise ValueError('Number of frames must be a positive number.')

    # Iterate to capture one frame
    for i in range(num_frames):
        # Pause the simulation
        simulation_mgr.pause_simulation(bng)
        # Advance the simulation by the corresponding number of seconds
        simulation_mgr.step_simulation_seconds(bng, capture_period_s)
        try:
            # Resume the simulation
            bng.resume()
        except ConnectionResetError:
            # Unable to reconnect with simulation
            logging_msg = 'Connection to simulator reset. Stopping script.'
            logging_mgr.log_error(logging_msg)
            break

        frame_dir = utils.create_frame_output_dir(output_dir, i)

        # Save camera sensor data to the frame directory
        data_capture_mgr.save_camera_image_data(sensor_camera, frame_dir)

        # Extract, combine and save the metadata to the frame directory
        camera_metadata = data_capture_mgr.extract_camera_metadata(sensor_camera)
        vehicle_metadata = data_capture_mgr.extract_vehicle_metadata(ego)
        imu_metadata = data_capture_mgr.extract_imu_data(sensor_imu)

        metadata_array = [camera_metadata,
                          imu_metadata,
                          vehicle_metadata]
        frame_metadata = utils.combine_dict(metadata_array)

        data_capture_mgr.save_metadata(frame_metadata, frame_dir)
        simulation_mgr.display_message(bng, f'Frame {i} captured.')
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
