import os
import utils
from typing import Dict, List

from beamngpy.types import Float3, Quat

# General variables
# - Here are defined the general variables used by the application
beamng_host: str = 'localhost'
beamng_port: int = 25252
random_seed: int = utils.get_time() # Can be set to a specific value for reproducibility
simulation_steps_per_second: int = 60
force_capture_freq_hz: bool = True
min_non_force_capture_freq_hz: float = 2
wait_for_frame_sleep_time_s: float = 0.01

# Paths
# - Here are defined the paths used by the application
beamng_home_path: str = os.getenv('BNG_HOME')
weather_presets_path: str = os.path.join(beamng_home_path, 'gameengine.zip/art/weather/defaults.json')
output_root_path: str = utils.return_documents_path()

# Sessions
# - Here are defined the session settings used by the application
default_map: str = 'west_coast_usa'
default_scenario: str = 'default_scenario'
default_start_delay_s: int = 15
default_duration_s: int = 10
default_capture_freq_hz: float = 5
default_weather: str = 'clear'
default_num_ai_traffic_vehicles: int = 20

# Time
# - Here are defined the time settings used by the application
night_time_start: str = '17:30:00'
night_time_end: str = '06:30:00'
play_time: bool = True
day_scale: float = 1.0
night_scale: float = 1.0
day_length_s: float = 600

# Vehicles
# - Here are defined the vehicle settings used by the application
default_vehicle_name: str = 'ego'
default_vehicle_model: str = 'etk800'
default_vehicle_initial_position: Float3 = (-720, 100, 119)
default_vehicle_initial_rotation: Quat = (0, 0, 0.35, 0.90)
supported_models: List[str] = [
    'autobello',
    'barstow',
    'bastion',
    'bluebuck',
    'bolide',
    'burnside',
    'bx',
    'covet',
    'etk800',
    'etkc',
    'etki',
    'fullsize',
    'hopper',
    'lansdale',
    'legran',
    'midsize',
    'miramar',
    'moonhawk',
    'nine',
    'pessima',
    'pickup',
    'sbr',
    'scintilla',
    'vivace',
    'wendover'
    ]
headlights_intensity: int = 1

# Cameras
# - Here are defined the camera settings used by the application
default_camera_name: str = 'sensor_camera'
default_camera_resolution: Float3 = (1280, 720)
default_camera_render_flags: Dict[str, bool] = {
    'colour': True,
    'annotation': True,
    'depth': True
    }
default_camera_position: Float3 = (0, -0.5, 1.5)
default_camera_fov_y: int = 70
default_camera_near_far_planes: tuple = (0.1, 1000.0)

# IMU
# - Here are defined the IMU settings used by the application
default_imu_position: Float3 = (0, 0, 0.5)
default_accel_window_width: float = 50.0
default_gyro_window_width: float = 50.0