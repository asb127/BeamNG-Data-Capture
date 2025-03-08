import data_capture_mgr, logging_mgr, scenario_mgr, session_config, settings, simulation_mgr, vehicle_mgr, utils

# Set random seed for reproducibility
utils.set_random_seed(settings.random_seed)

# Create an output directory to store the session data
output_dir = utils.create_output_dir(settings.output_root_path)

# Set up logging for the data capture process
logging_mgr.configure_logging(output_dir)

try:
    # Create the session configuration
    session = session_config.create_session_config()
    # Validate the session configuration
    session.validate()
except ValueError as e:
    # A value error occurred while creating the session configuration, the capture session is aborted
    logging_mgr.log_error(f'Value error creating session configuration, aborting capture session: {e}')
    quit()

# Refresh the available weather presets
scenario_mgr.get_weather_presets()

# Create BeamNGpy instance and connect to the simulator
bng = simulation_mgr.launch_beamng()

# Set simulation steps per second
simulation_mgr.set_simulation_steps_per_second(bng, settings.simulation_steps_per_second)

# Create a scenario and vehicle for the capture session using the session configuration
scenario, ego = scenario_mgr.create_scenario(bng, session)

# Initialize the scenario in the simulator with the specified number of AI traffic vehicles
scenario_mgr.initialize_scenario(bng,
                                 scenario,
                                 ego,
                                 session)

# Create all camera sensors configured for the capture session
camera_list = []
for camera_config in session.cameras:
    # Create camera sensor and attach it to the vehicle
    camera_sensor = data_capture_mgr.create_camera_sensor(bng,
                                                          ego,
                                                          camera_config)
    # Add the camera sensor to the list
    camera_list.append(camera_sensor)
    # Extract and store the camera sensor metadata
    camera_metadata = camera_config.extract_camera_metadata()

# Log a warning if no camera sensors are created for the capture session
if not camera_list:
    logging_mgr.log_warning('No camera sensors created for the capture session.')

# Create an IMU sensor and attach it to the vehicle
sensor_imu = data_capture_mgr.create_imu_sensor(bng,
                                                ego,
                                                'sensor_imu')

try:
    # Send vehicle to random waypoint in the scenario to start the capture session
    scenario_mgr.teleport_vehicle_to_random_waypoint(bng,
                                                     scenario,
                                                     ego)

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
    
    # Extract and save general session metadata 
    session_metadata = session.extract_session_metadata()
    data_capture_mgr.save_metadata(session_metadata, output_dir, 'session_metadata.json')

    # Initialize variables used for night-time checks
    headlights_on = False
    night_time_start = utils.hhmmss_to_beamng_time(settings.night_time_start)
    night_time_end = utils.hhmmss_to_beamng_time(settings.night_time_end)

    # Set the time of day settings for the session
    simulation_mgr.set_time_of_day(bng,
                                   play=settings.play_time,
                                   day_scale=settings.day_scale,
                                   night_scale=settings.night_scale,
                                   day_length=settings.day_length_s)

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

        # Check time of day
        time_of_day = simulation_mgr.get_time_of_day(bng)
        # If it's night, turn on the headlights
        if ((time_of_day['time'] < night_time_end or time_of_day['time'] > night_time_start)
                and not headlights_on):
            vehicle_mgr.set_headlights(ego, settings.headlights_intensity)
            headlights_on = True
        # If it's day, turn off the headlights
        elif (time_of_day['time'] >= night_time_end and time_of_day['time'] <= night_time_start
                and headlights_on):
            vehicle_mgr.set_headlights(ego, 0)
            headlights_on = False

        # Create a directory for the frame output
        frame_dir = utils.create_frame_output_dir(output_dir, i)

        # For each camera sensor, save the data
        for camera_sensor in camera_list:
            # Create a directory for the camera sensor inside the frame directory
            camera_dir = utils.create_dir(frame_dir, camera_sensor.name)
            # Save the camera sensor data into the camera directory
            data_capture_mgr.save_camera_image_data(camera_sensor, camera_dir)

        # Extract, combine and save the metadata to the frame directory
        frame_metadata_list = []
        frame_metadata_list.append(data_capture_mgr.extract_time_of_day_metadata(bng))
        frame_metadata_list.append(data_capture_mgr.extract_vehicle_metadata(ego))
        frame_metadata_list.append(data_capture_mgr.extract_imu_data(sensor_imu))
        frame_metadata_dict = utils.combine_dict(frame_metadata_list)

        data_capture_mgr.save_metadata(frame_metadata_dict, frame_dir)
        simulation_mgr.display_message(bng, f'Frame {i} captured.')
except KeyboardInterrupt:
    # User stopped the simulation process
    logging_mgr.log_action('Simulation stopped by user.')
except ValueError as e:
    # A value error stopped the simulation process
    logging_mgr.log_error(f'Simulation stopped by a value error: {e}')
except Exception as e:
    # An unexpected error stopped the simulation process
    logging_mgr.log_error(f'Simulation stopped by an unexpected error: {e}')
finally:
    # Simulation finished, close
    logging_mgr.log_action('Simulation finished.')
    simulation_mgr.close_beamng(bng)
