import os, json
from datetime import datetime
from beamngpy.sensors import Camera, AdvancedIMU

import logging_mgr

def create_output_dir():
    # Create a directory to store the captured images
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = os.path.join(os.path.expanduser('~'),
                              'Documents',
                              'BeamNG-Data-Capture',
                              timestamp)
    os.makedirs(output_dir, exist_ok=True)
    logging_mgr.log_action(f'Output directory created at {output_dir}.')
    return output_dir

def create_frame_output_dir(output_dir, i):
    # Create a subfolder for every frame
    frame_dir = os.path.join(output_dir, f'frame_{i}')
    os.makedirs(frame_dir, exist_ok=True)
    logging_mgr.log_action(f'Frame {i} output directory created at {output_dir}.')
    return frame_dir

def create_camera_sensor(bng,
                         vehicle,
                         name,
                         pos,
                         resolution,
                         is_render_colours,
                         is_render_annotations,
                         is_render_depth):
    # Create a camera sensor attached to the vehicle
    sensor_camera = Camera(name=name,
                           bng=bng,
                           vehicle=vehicle,
                           pos=pos,
                           resolution=resolution,
                           is_render_colours=is_render_colours,
                           is_render_annotations=is_render_annotations,
                           is_render_depth=is_render_depth)
    return sensor_camera

def create_imu_sensor(bng, vehicle, name):
    # Create an Inertial Measurement Unit (IMU) sensor attached to the vehicle
    sensor_imu = AdvancedIMU(name=name,
                             bng=bng,
                             vehicle=vehicle,
                             is_send_immediately=True)
    return sensor_imu

def save_camera_image_data(camera, output_dir):
    # Poll the camera sensor
    sensor_data = camera.poll()
    logging_mgr.log_action(f'Camera "{camera.name}" data polled.')

    # Split the sensor data
    color_image = sensor_data['colour']
    depth_image = sensor_data['depth']
    semantic_image = sensor_data['annotation']

    # Remove alpha channel from color image
    color_image = color_image.convert('RGB')

    # Save the images to the output directory
    color_image.save(os.path.join(output_dir, 'color.png'))
    depth_image.save(os.path.join(output_dir, 'depth.png'))
    semantic_image.save(os.path.join(output_dir, 'semantic.png'))
    logging_mgr.log_action(f'Camera "{camera.name}" data saved in "{output_dir}".')

def extract_imu_data(imu):
    # Extract data from the IMU sensor into a dictionary
    imu_data = imu.poll()

    # Extract specific data from the IMU sensor
    imu_data_concise = {
        'acceleration': imu_data.accSmooth,
        'angular_acceleration': imu_data.angAccel,
        'angular_velocity': imu_data.angVelSmooth
    }

    return imu_data_concise

def extract_vehicle_metadata(vehicle):
    vehicle.sensors.poll()

    state_data = vehicle.sensors['state']

    # Extract metadata from the vehicle into a dictionary
    metadata = {
        'time': state_data['time'],
        'linear_velocity': state_data['vel'],
        'direction': state_data['dir'],
        'position': state_data['pos']
    }
    return metadata

def extract_camera_metadata(camera):
    # Extract metadata from the camera sensor into a dictionary
    metadata = {
        'fov': camera.fovY,
        'resolution': camera.resolution,
        'position': camera.pos
    }
    return metadata

def combine_metadata(vehicle_metadata, camera_metadata):
    # Combine all metadata into a single dictionary
    # TODO
    metadata = {**vehicle_metadata, **camera_metadata}
    
    return metadata

def save_metadata(metadata, output_dir):
    # Save metadata to a JSON file
    metadata_file = os.path.join(output_dir, 'metadata.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    logging_mgr.log_action(f'Metadata saved in "{metadata_file}".')
