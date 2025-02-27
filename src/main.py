import data_capture_mgr, simulation_mgr, scenario_mgr, logging_mgr, session_config, utils

# Create an output directory to store the session data
root_dir = utils.return_documents_path()
output_dir = utils.create_output_dir(root_dir)

# Set up logging for the data capture process
logging_mgr.configure_logging(output_dir)

# Create the session configuration
session = session_config.create_session_config()

# Create BeamNGpy instance and connect to the simulator
bng = simulation_mgr.launch_beamng('localhost', 25252)

# Set simulation steps per second to 60
simulation_mgr.set_simulation_steps_per_second(bng, 60)

# Create a scenario and vehicle for the capture session usign the session configuration
scenario, ego = scenario_mgr.create_scenario(bng,
                                             session.map,
                                             session.name,
                                             session.vehicle.name,
                                             session.vehicle.model,
                                             session.vehicle.initial_position,
                                             session.vehicle.initial_rotation)

# Initialize the scenario in the simulator
scenario_mgr.initialize_scenario(bng,
                                 scenario,
                                 ego)

# Create all camera sensors configured for the capture session
camera_list = []
camera_metadata_list = []
for camera_config in session.cameras:
    # Create camera sensor and attach it to the vehicle
    camera_sensor = data_capture_mgr.create_camera_sensor(bng,
                                                          ego,
                                                          camera_config.name,
                                                          camera_config.position,
                                                          camera_config.resolution,
                                                          camera_config.is_render_colours,
                                                          camera_config.is_render_annotations,
                                                          camera_config.is_render_depth,
                                                          camera_config.fov_y)
    # Add the camera sensor to the list
    camera_list.append(camera_sensor)
    # Extract and store the camera sensor metadata
    camera_metadata = data_capture_mgr.extract_camera_metadata(camera_sensor)
    # Add the camera sensor metadata to the list
    camera_metadata_list.append(camera_metadata)

# Log a warning if no camera sensors are created for the capture session
if (len(camera_list) == 0):
    logging_mgr.log_warning('No camera sensors created for the capture session.')

# Create an IMU sensor and attach it to the vehicle
sensor_imu = data_capture_mgr.create_imu_sensor(bng,
                                                ego,
                                                'sensor_imu')

try:
    # Set up session parameters
    session_length_s = session.duration_s
    capture_freq_hz = session.capture_freq_hz

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
    
    # Save general session metadata (not frame-specific)
    # TO DO


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

        # For each camera sensor, save the data
        for camera_sensor in camera_list:
            # Create a directory for the camera sensor inside the frame directory
            camera_dir = utils.create_dir(frame_dir, camera_sensor['camera'].name)
            # Save the camera sensor data
            data_capture_mgr.save_camera_image_data(camera_sensor, frame_dir)

        # Extract, combine and save the metadata to the frame directory
        vehicle_metadata = data_capture_mgr.extract_vehicle_metadata(ego)
        imu_metadata = data_capture_mgr.extract_imu_data(sensor_imu)

        metadata_array = [imu_metadata,
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
