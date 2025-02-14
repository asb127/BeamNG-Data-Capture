import os
from datetime import datetime
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Camera

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
scenario.add_vehicle(vehicle, pos=(-720, 100, 120), rot_quat=(0, 0, 0.35, 0.90))
# Place files defining our scenario for the simulator to read
scenario.make(bng)

# Load and start our scenario
bng.scenario.load(scenario)
bng.scenario.start()
# Make the vehicle's AI follow the lane
vehicle.ai.set_mode('span')

# Create camera sensors and attach them to the vehicle (Try combining into one?)
sensor_camera = Camera(name='sensor_camera', bng=bng, vehicle=vehicle, pos=(0, -0.5, 1.5), resolution=(1280, 720), is_render_colours=True, is_render_annotations=True, is_render_depth=True)

# Create a directory to store the captured images
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
output_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'BeamNG-Data-Capture', timestamp)
os.makedirs(output_dir, exist_ok=True)

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
        
        sensor_camera_data = sensor_camera.poll()

        # Split camera data
        color_image = sensor_camera_data['colour']
        depth_image = sensor_camera_data['depth']
        semantic_image = sensor_camera_data['annotation']

        # Remove alpha channel from color image
        color_image = color_image.convert('RGB') 
        
        # Create a subfolder for every frame
        frame_dir = os.path.join(output_dir, f'frame_{i}')
        os.makedirs(frame_dir, exist_ok=True)
        
        # Save the images to the subfolder
        color_image.save(os.path.join(frame_dir, 'color.png'))
        depth_image.save(os.path.join(frame_dir, 'depth.png'))
        semantic_image.save(os.path.join(frame_dir,'semantic.png'))
except KeyboardInterrupt:
    # User stopped the simulation process
    print('Simulation stopped by user')
finally:
    # Simulation finished, close
    print('Simulation finished')
    bng.close()
