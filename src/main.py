from beamngpy.sensors import Camera

import data_capture, simulation_mgr, scenario_mgr

# Create BeamNGpy instance and connect to the simulator
bng = simulation_mgr.launch_beamng('localhost', 25252)

# Set simulation steps per second to 60
simulation_mgr.set_simulation_steps_per_second(bng, 60)

# Create a scenario and vehicle for the capture session
scenario, ego = scenario_mgr.create_scenario(bng, 'west_coast_usa', 'capture_scenario', 'ego', 'etk800', (-720, 100, 119), (0, 0, 0.35, 0.90))

# Initialize the scenario in the simulator
scenario_mgr.initialize_scenario(bng, scenario, ego)

# Create camera sensors and attach them to the vehicle
sensor_camera = Camera(name='sensor_camera', bng=bng, vehicle=ego, pos=(0, -0.5, 1.5), resolution=(1280, 720), is_render_colours=True, is_render_annotations=True, is_render_depth=True)

# Create an output directory to store the captured data
output_dir = data_capture.create_output_dir()

try:
    # Capture 10 images, one every 10 seconds
    num_frames = 10
    wait_seconds = 10

    # Iterate to capture one frame
    for i in range(num_frames):
        # Pause the simulation
        bng.pause()
        # Advance the simulation by the corresponding number of steps
        bng.step(simulation_mgr.simulation_steps_per_second * wait_seconds)  
        try:
            # Resume the simulation
            bng.resume()
        except ConnectionResetError:
            # Unable to reconnect with simulation
            print('Connection to simulator reset. Stopping script.')
            break

        frame_dir = data_capture.create_frame_output_dir(output_dir, i)
        data_capture.save_camera_data(sensor_camera, frame_dir)
        bng.ui.display_message(f'Frame {i} captured')
except KeyboardInterrupt:
    # User stopped the simulation process
    print('Simulation stopped by user')
finally:
    # Simulation finished, close
    print('Simulation finished')
    bng.close()