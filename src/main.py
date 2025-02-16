import data_capture_mgr, simulation_mgr, scenario_mgr

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

# Create camera sensors and attach them to the vehicle
sensor_camera = data_capture_mgr.create_camera_sensor(bng,
                                                      ego,
                                                      'sensor_camera',
                                                      (0, -0.5, 1.5),
                                                      (1280, 720),
                                                      True,
                                                      True,
                                                      True)

# Create an output directory to store the captured data
output_dir = data_capture_mgr.create_output_dir()

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
            simulation_mgr.resume_simulation(bng)
        except ConnectionResetError:
            # Unable to reconnect with simulation
            print('Connection to simulator reset. Stopping script.')
            break

        frame_dir = data_capture_mgr.create_frame_output_dir(output_dir, i)
        data_capture_mgr.save_camera_data(sensor_camera, frame_dir)
        simulation_mgr.display_message(bng, f'Frame {i} captured')
except KeyboardInterrupt:
    # User stopped the simulation process
    print('Simulation stopped by user')
finally:
    # Simulation finished, close
    print('Simulation finished')
    simulation_mgr.close_beamng(bng)
