from beamngpy.sensors import Camera, AdvancedIMU
from beamngpy import BeamNGpy
from beamngpy.vehicle import Vehicle

import logging_mgr, simulation_mgr, utils
from camera_sensor_config import CameraSensorConfig
from beamngpy.types import StrDict

def create_camera_sensor(bng: BeamNGpy,
                         vehicle: Vehicle,
                         camera: CameraSensorConfig) -> Camera:
    # Create a camera sensor attached to the vehicle
    sensor_camera = Camera(name=camera.name,
                           bng=bng,
                           vehicle=vehicle,
                           pos=camera.position,
                           resolution=camera.resolution,
                           field_of_view_y=camera.fov_y,
                           is_render_colours=camera.is_render_colours,
                           is_render_annotations=camera.is_render_annotations,
                           is_render_depth=camera.is_render_depth)
    # Return the camera sensor and its field of view
    return sensor_camera

def create_imu_sensor(bng: BeamNGpy,
                      vehicle: Vehicle,
                      name: str) -> AdvancedIMU:
    # Create an Inertial Measurement Unit (IMU) sensor attached to the vehicle
    sensor_imu = AdvancedIMU(name=name,
                             bng=bng,
                             vehicle=vehicle,
                             is_send_immediately=True)
    return sensor_imu

def save_camera_image_data(camera: Camera, output_dir: str) -> None:
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
    color_image.save(utils.join_paths(output_dir, 'color.png'))
    depth_image.save(utils.join_paths(output_dir, 'depth.png'))
    semantic_image.save(utils.join_paths(output_dir, 'semantic.png'))
    logging_mgr.log_action(f'Camera "{camera.name}" data saved in "{output_dir}".')

def extract_imu_data(imu: AdvancedIMU) -> StrDict:
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

def extract_vehicle_metadata(vehicle: Vehicle) -> StrDict:
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

def extract_vehicle_simulation_time(vehicle: Vehicle) -> float:
    # Poll the vehicle sensors
    vehicle.sensors.poll()
    logging_mgr.log_action(f'Vehicle "{vehicle.vid}" sensors polled.')

    # Extract state data from the vehicle
    state_data = vehicle.sensors['state']
    logging_mgr.log_action(f'Vehicle "{vehicle.vid}" state data extracted.')

    # Extract simulation time from the vehicle
    simulation_time = state_data['time']
    logging_mgr.log_action(f'Vehicle "{vehicle.vid}" simulation time extracted: {simulation_time} seconds.')

    return simulation_time

def extract_time_of_day_metadata(bng: BeamNGpy) -> StrDict:
    '''Extract time of day metadata from the simulator.'''
    time_of_day = simulation_mgr.get_time_of_day(bng)
    # Extract time of day metadata into a dictionary
    metadata = {
        'time_of_day': time_of_day['timeStr']
    }
    logging_mgr.log_action('Time of day metadata extracted.')
    return metadata

def save_metadata(metadata: dict,
                  output_dir: str,
                  file_name = 'metadata.json') -> None:
    # Save metadata to a JSON file
    utils.save_json_file(metadata,
                         output_dir,
                         file_name)
    logging_mgr.log_action(f'Metadata saved in "{output_dir}".')