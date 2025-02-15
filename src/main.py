from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Camera

import data_capture

# Instantiate BeamNGpy instance connecting to the simulator on the given host and port
bng = BeamNGpy('localhost', 25252)
# Launch the simulator
bng.open()
# Set simulation steps per second to 60
steps_per_second = 60
bng.set_steps_per_second(steps_per_second)
# Create a scenario in a given map
scenario = Scenario('west_coast_usa', 'capture_scenario')
# Create a vehicle to capture data from
vehicle = Vehicle('ego', model='etk800')
# Add it to our scenario at this position and rotation
scenario.add_vehicle(vehicle, pos=(-720, 100, 119), rot_quat=(0, 0, 0.35, 0.90))
# Place files defining our scenario for the simulator to read
scenario.make(bng)

# Load and start our scenario
bng.scenario.load(scenario)
bng.scenario.start()
# Make the vehicle's AI follow the lane
vehicle.ai.set_mode('span')

# Create camera sensors and attach them to the vehicle (Try combining into one?)
sensor_camera = Camera(name='sensor_camera', bng=bng, vehicle=vehicle, pos=(0, -0.5, 1.5), resolution=(1280, 720), is_render_colours=True, is_render_annotations=True, is_render_depth=True)

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
        bng.step(steps_per_second * wait_seconds)  
        try:
            # Resume the simulation
            bng.resume()
        except ConnectionResetError:
            # Unable to reconnect with simulation
            print('Connection to simulator reset. Stopping script.')
            break

        frame_dir = data_capture.create_frame_output_dir(output_dir, i)
        data_capture.save_camera_data(sensor_camera, frame_dir)
except KeyboardInterrupt:
    # User stopped the simulation process
    print('Simulation stopped by user')
finally:
    # Simulation finished, close
    print('Simulation finished')
    bng.close()
