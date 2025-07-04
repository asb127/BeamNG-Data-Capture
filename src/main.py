import time

import data_capture_mgr, gui_mgr, logging_mgr, scenario_mgr, session_config, settings, simulation_mgr, vehicle_mgr, utils
from gui_tkinter import TkinterGuiApi

# Create an output directory to store the session data
output_dir = utils.create_output_dir(settings.output_root_path)

# Set up logging for the data capture process
logging_mgr.configure_logging(output_dir)

gui_mgr.set_gui_api(TkinterGuiApi())

session = gui_mgr.get_session_config()
if session is None:
    # User cancelled the session configuration, exit the program
    logging_mgr.log_action('Session configuration window closed without requesting capture session, quitting.')
    exit(0)

# Set random seed for reproducibility
utils.set_random_seed(settings.random_seed)

# Refresh the available weather presets
scenario_mgr.get_weather_presets()

# Create BeamNGpy instance and connect to the simulator
bng = simulation_mgr.launch_beamng()

# Set simulation steps per second
simulation_mgr.set_deterministic_steps_per_second(bng, settings.simulation_steps_per_second)
simulation_mgr.pause_simulation(bng)

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
    # If a starting waypoint was assigned, teleport vehicle to it
    if (session.starting_waypoint):
        scenario_mgr.teleport_vehicle_to_waypoint(bng,
                                                  scenario,
                                                  ego,
                                                  session.starting_waypoint)

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
    try:
        night_time_start = utils.hhmmss_to_beamng_time(settings.night_time_start)
        night_time_end = utils.hhmmss_to_beamng_time(settings.night_time_end)
    except ValueError as e:
        utils.log_and_show_error(str(e))
        exit(1)
    # Set the time of day settings for the session
    simulation_mgr.set_time_of_day(bng,
                                   time_of_day=session.time,
                                   play=settings.play_time,
                                   day_scale=settings.day_scale,
                                   night_scale=settings.night_scale,
                                   day_length=settings.day_length_s)

    # Initialize minimum start delay
    start_delay_s = 1
    if (settings.default_start_delay_s > start_delay_s):
        start_delay_s = settings.default_start_delay_s
    # Skip initial seconds to allow the simulation to stabilize
    simulation_mgr.step_simulation_seconds(bng, start_delay_s)

    # Check if the capture frequency should be forced
    force_capture_freq_hz = settings.force_capture_freq_hz
    # If capture frequency is lower than the minimum non-force capture frequency value, force it
    if capture_freq_hz < settings.min_non_force_capture_freq_hz:
        force_capture_freq_hz = True
    
    # If the capture frequency is not forced, resume simulation
    if not force_capture_freq_hz:
        simulation_mgr.resume_simulation(bng)

    # Main capture loop and logic
    frame_metadata_list = []
    for cur_frame_num in range(num_frames):
        # Check time of day
        time_of_day = simulation_mgr.get_time_of_day(bng)
        is_night_time = night_time_start <= time_of_day['time'] < night_time_end
        # If it's night, turn on the headlights
        if is_night_time and not headlights_on:
            vehicle_mgr.set_headlights(ego, settings.headlights_intensity)
            headlights_on = True
        # If it's day, turn off the headlights
        elif not is_night_time and headlights_on:
            vehicle_mgr.set_headlights(ego, 0)
            headlights_on = False

        # Extract and save the data from all camera sensors
        data_capture_mgr.save_all_camera_image_data(camera_list, output_dir, cur_frame_num)

        # Extract, combine and save the metadata to the frame directory
        vehicle_metadata = data_capture_mgr.extract_vehicle_metadata(ego)
        frame_metadata = {}
        frame_metadata.update({'frame': cur_frame_num})
        frame_metadata.update(data_capture_mgr.extract_time_of_day_metadata(bng))
        frame_metadata.update(vehicle_metadata)
        frame_metadata.update(data_capture_mgr.extract_imu_data(sensor_imu))
        frame_metadata_list.append(frame_metadata)

        simulation_mgr.display_message(bng, f'Frame {cur_frame_num} captured.')

        # Use the 'ego' vehicle metadata to check the current simulation time
        current_sim_time_s = data_capture_mgr.extract_vehicle_simulation_time_from_metadata(vehicle_metadata)

        # Update the last capture time to the current simulation time
        last_capture_time_s = current_sim_time_s
        
        # If not on the last captured frame, advance time by the capture period
        if cur_frame_num < (num_frames - 1):
            if force_capture_freq_hz:
                # If capture frequency is forced
                # Advance the simulation by the corresponding number of seconds for the capture period
                simulation_mgr.step_simulation_seconds(bng, capture_period_s)
            else:
                # If capture frequency is not forced
                # Wait until it's time to capture the next frame

                # Update the current simulation time and last frame period
                current_sim_time_s = data_capture_mgr.extract_vehicle_simulation_time_from_metadata(vehicle_metadata)
                last_frame_period_s = current_sim_time_s - last_capture_time_s
                logging_mgr.log_action(f'Current simulation time: {current_sim_time_s} s, last frame period: {last_frame_period_s} s.')

                if last_frame_period_s > capture_period_s:
                    # Log a warning that the capture frequency is too high
                    logging_mgr.log_warning(f"""Capture frequency too high for frame {cur_frame_num}.
                                            \nPrevious capture took {last_frame_period_s} seconds.
                                            \nCapture period is {capture_period_s} seconds.""")
                else:
                    # If the capture period hasn't passed yet, wait until it does
                    while last_frame_period_s < capture_period_s:
                        # Wait for a short time before checking the simulation time again
                        time.sleep(settings.wait_for_frame_sleep_time_s)
                        # Update the vehicle metadata
                        vehicle_metadata = data_capture_mgr.extract_vehicle_metadata(ego)
                        # Update the current simulation time and last frame period
                        current_sim_time_s = data_capture_mgr.extract_vehicle_simulation_time_from_metadata(vehicle_metadata)
                        last_frame_period_s = current_sim_time_s - last_capture_time_s

    # After capture loop, save all frame metadata in a single file
    data_capture_mgr.save_metadata(frame_metadata_list, output_dir, 'frames_metadata.json')

except KeyboardInterrupt:
    utils.log_and_show_error('Simulation stopped by user.')
except ValueError as e:
    utils.log_and_show_error(f'Simulation stopped by a value error: {e}')
    exit(1)
finally:
    # Simulation finished, close
    logging_mgr.log_action('Simulation finished.')
    simulation_mgr.close_beamng(bng)
