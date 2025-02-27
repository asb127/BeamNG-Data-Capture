import os, json
from beamngpy.sensors import Camera, AdvancedIMU
from beamngpy import BeamNGpy
from beamngpy.vehicle import Vehicle

import logging_mgr

def create_camera_sensor(bng: BeamNGpy,
                         vehicle: Vehicle,
                         name: str,
                         pos: tuple,
                         resolution: tuple,
                         is_render_colours: bool,
                         is_render_annotations: bool,
                         is_render_depth: bool,
                         fov_y: int = 70) -> dict:
    # Create a camera sensor attached to the vehicle
    sensor_camera = Camera(name=name,
                           bng=bng,
                           vehicle=vehicle,
                           pos=pos,
                           resolution=resolution,
                           field_of_view_y=fov_y,
                           is_render_colours=is_render_colours,
                           is_render_annotations=is_render_annotations,
                           is_render_depth=is_render_depth)
    # Return the camera sensor and its field of view
    return {'camera': sensor_camera, 'fov_y': fov_y}

def create_imu_sensor(bng: BeamNGpy,
                      vehicle: Vehicle,
                      name: str) -> AdvancedIMU:
    # Create an Inertial Measurement Unit (IMU) sensor attached to the vehicle
    sensor_imu = AdvancedIMU(name=name,
                             bng=bng,
                             vehicle=vehicle,
                             is_send_immediately=True)
    return sensor_imu

def save_camera_image_data(camera_dict: dict, output_dir: str) -> None:
    # Extract the camera sensor from the received dictionary
    camera = camera_dict['camera']
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

def extract_imu_data(imu: AdvancedIMU) -> dict:
    # Extract data from the IMU sensor into a dictionary
    imu_data = imu.poll()
    logging_mgr.log_action(f'IMU "{imu.name}" data polled.')

    # Extract specific data from the IMU sensor
    imu_data_concise = {
        'acceleration': imu_data['accSmooth'],
        'angular_acceleration': imu_data['angAccel'],
        'angular_velocity': imu_data['angVelSmooth']
    }

    logging_mgr.log_action(f'IMU "{imu.name}" metadata extracted.')

    return imu_data_concise

def extract_vehicle_metadata(vehicle: Vehicle) -> dict:
    # Poll the vehicle sensors
    vehicle.sensors.poll()
    logging_mgr.log_action(f'Vehicle "{vehicle.vid}" sensors polled.')

    # Extract state data from the vehicle
    state_data = vehicle.sensors['state']
    logging_mgr.log_action(f'Vehicle "{vehicle.vid}" state data extracted.')

    # Extract metadata from the vehicle into a dictionary
    metadata = {
        'time': state_data['time'],
        'linear_velocity': state_data['vel'],
        'direction': state_data['dir'],
        'position': state_data['pos']
    }
    logging_mgr.log_action(f'Vehicle "{vehicle.vid}" metadata extracted.')

    return metadata

def extract_camera_metadata(camera_dict: dict) -> dict:
    # Split the camera dictionary into the camera sensor and its field of view
    camera = camera_dict['camera']
    fov_y = camera_dict['fov_y']

    # Extract metadata from the camera sensor into a dictionary
    metadata = {
        'fov': fov_y,
        'resolution': camera.resolution,
        'near_far_planes': camera.near_far_planes
    }
    logging_mgr.log_action(f'Camera "{camera.name}" metadata extracted.')

    return metadata

def combine_metadata(metadata_array: list) -> dict:
    # Combine all metadata into a single dictionary
    combined_metadata = {}
    for metadata in metadata_array:
        combined_metadata.update(metadata)
    logging_mgr.log_action('Metadata array combined.')
    return combined_metadata

def save_metadata(metadata: dict, output_dir: str) -> None:
    # Save metadata to a JSON file
    metadata_file = os.path.join(output_dir, 'metadata.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata,
                  f,
                  indent=4)
    logging_mgr.log_action(f'Metadata saved in "{metadata_file}".')
