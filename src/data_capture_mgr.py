from concurrent.futures import ThreadPoolExecutor, as_completed
from beamngpy.sensors import Camera, AdvancedIMU
from beamngpy import BeamNGpy
from beamngpy.vehicle import Vehicle

import logging_mgr, simulation_mgr, utils
from camera_sensor_config import CameraSensorConfig
from type_defs import StrDict

def create_camera_sensor(bng: BeamNGpy,
                         vehicle: Vehicle,
                         camera: CameraSensorConfig) -> Camera:
    """Create a camera sensor attached to the vehicle."""
    sensor_camera = Camera(name=camera.name,
                           bng=bng,
                           vehicle=vehicle,
                           pos=camera.position,
                           dir=camera.direction,
                           up=camera.up_vector,
                           resolution=camera.resolution,
                           field_of_view_y=camera.fov_y,
                           near_far_planes=camera.near_far_planes,
                           is_render_colours=camera.is_render_colours,
                           is_render_annotations=camera.is_render_annotations,
                           is_render_depth=camera.is_render_depth)
    return sensor_camera

def create_imu_sensor(bng: BeamNGpy,
                      vehicle: Vehicle,
                      name: str) -> AdvancedIMU:
    """Create an Inertial Measurement Unit (IMU) sensor attached to the vehicle."""
    import settings
    sensor_imu = AdvancedIMU(name=name,
                             bng=bng,
                             vehicle=vehicle,
                             pos=settings.default_imu_position,
                             accel_window_width=settings.default_accel_window_width,
                             gyro_window_width=settings.default_gyro_window_width,
                             is_send_immediately=True)
    return sensor_imu

def save_camera_image_data(camera: Camera, output_dir: str, frame_num: int) -> None:
    """Poll the camera sensor and save its image data to local storage."""
    sensor_data = camera.poll()
    logging_mgr.log_action(f'Camera "{camera.name}" data polled.')

    try:
        frame_str = f"{frame_num:05d}"
        if getattr(camera, "is_render_colours", False):
            color_image = sensor_data['colour'].convert('RGB')
            color_path = utils.join_paths(output_dir, f'frame_{frame_str}_{camera.name}_color.png')
            color_image.save(color_path)
        if getattr(camera, "is_render_depth", False):
            depth_image = sensor_data['depth']
            depth_path = utils.join_paths(output_dir, f'frame_{frame_str}_{camera.name}_depth.png')
            depth_image.save(depth_path)
        if getattr(camera, "is_render_annotations", False):
            semantic_image = sensor_data['annotation']
            semantic_path = utils.join_paths(output_dir, f'frame_{frame_str}_{camera.name}_semantic.png')
            semantic_image.save(semantic_path)
    except Exception as e:
        logging_mgr.log_error(f'Error saving image for camera {camera.name}: {e}')

    logging_mgr.log_action(f'Camera "{camera.name}" data saved for frame {frame_num} in "{output_dir}".')

def save_all_camera_image_data(camera_list, output_dir, frame_num):
    """Extract and save all camera image data in parallel from a list of camera sensors."""
    with ThreadPoolExecutor() as executor:
        futures = []
        for camera_sensor in camera_list:
            futures.append(executor.submit(save_camera_image_data, camera_sensor, output_dir, frame_num))
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging_mgr.log_error(f'Error saving camera data: {e}')

def extract_imu_data(imu: AdvancedIMU) -> StrDict:
    """Extract data from the IMU sensor into a dictionary."""
    imu_data = imu.poll()
    logging_mgr.log_action(f'IMU "{imu.name}" data polled.')

    imu_data_concise = {
        'acceleration': imu_data['accSmooth'],
        'angular_acceleration': imu_data['angAccel'],
        'angular_velocity': imu_data['angVelSmooth']
    }

    logging_mgr.log_action(f'IMU "{imu.name}" metadata extracted.')

    return imu_data_concise

def extract_vehicle_metadata(vehicle: Vehicle) -> StrDict:
    """Extract metadata from the vehicle's sensors into a dictionary."""
    vehicle.sensors.poll()
    logging_mgr.log_action(f'Vehicle "{vehicle.vid}" sensors polled.')

    state_data = vehicle.sensors['state']
    logging_mgr.log_action(f'Vehicle "{vehicle.vid}" state data extracted.')

    metadata = {
        'time': state_data['time'],
        'linear_velocity': state_data['vel'],
        'direction': state_data['dir'],
        'position': state_data['pos']
    }
    logging_mgr.log_action(f'Vehicle "{vehicle.vid}" metadata extracted.')

    return metadata

def extract_vehicle_simulation_time_from_metadata(vehicle_metadata) -> float:
    """Extract the simulation time from the vehicle metadata."""
    return vehicle_metadata['time']

def extract_time_of_day_metadata(bng: BeamNGpy) -> StrDict:
    """Extract time of day metadata from the simulator."""
    time_of_day = simulation_mgr.get_time_of_day(bng)
    metadata = {
        'time_of_day': time_of_day['timeStr']
    }
    logging_mgr.log_action('Time of day metadata extracted.')
    return metadata

def save_metadata(metadata: dict,
                  output_dir: str,
                  file_name = 'metadata.json') -> None:
    """Save metadata to a JSON file."""
    utils.save_json_file(metadata,
                         output_dir,
                         file_name)
    logging_mgr.log_action(f'Metadata saved in "{output_dir}".')