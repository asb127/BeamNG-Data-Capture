from type_defs import TypedDict, List

import logging_mgr, utils
from vehicle_config import VehicleConfig
from camera_sensor_config import CameraSensorConfig

class SessionConfigDict(TypedDict):
    scenario: str
    duration_s: float
    capture_freq_hz: float
    map: str
    vehicle: VehicleConfig
    cameras: List[CameraSensorConfig]
    weather: str
    time: str
    num_ai_traffic_vehicles: int
    starting_waypoint: str

class SessionConfig:
    """Configuration class for a capture session."""
    def __init__(self,
                 scenario: str = None,
                 duration_s: float = None,
                 capture_freq_hz: float = None,
                 map_name: str = None,
                 vehicle: VehicleConfig = None,
                 cameras: List[CameraSensorConfig] = None,
                 weather: str = None,
                 time: str = None,
                 num_ai_traffic_vehicles: int = None,
                 starting_waypoint: str = ''):
        """Initialize a new session configuration with the provided parameters."""
        import settings
        self._scenario = scenario if scenario is not None else settings.default_scenario
        self._duration_s = duration_s if duration_s is not None else settings.default_duration_s
        self._capture_freq_hz = capture_freq_hz if capture_freq_hz is not None else settings.default_capture_freq_hz
        self._map = map_name if map_name is not None else settings.default_map
        self._vehicle = vehicle if vehicle is not None else VehicleConfig()
        self._cameras = cameras if cameras is not None else [CameraSensorConfig()]
        self._weather = weather if weather is not None else settings.default_weather
        self._time = time if time is not None else settings.time_of_day_start
        self._num_ai_traffic_vehicles = num_ai_traffic_vehicles if num_ai_traffic_vehicles is not None else settings.default_num_ai_traffic_vehicles
        self._starting_waypoint = starting_waypoint

    @property
    def scenario(self) -> str:
        """Get the scenario name of the session configuration."""
        return self._scenario

    @scenario.setter
    def scenario(self, scenario: str) -> None:
        """Set the scenario name of the session configuration."""
        self._scenario = scenario

    @property
    def duration_s(self) -> float:
        """Get the duration of the capture session (in seconds)."""
        return self._duration_s

    @duration_s.setter
    def duration_s(self, duration: float) -> None:
        """Set the duration of the capture session (in seconds)."""
        if duration <= 0:
            raise ValueError('Duration must be a positive number.')
        self._duration_s = duration

    @property
    def capture_freq_hz(self) -> float:
        """Get the capture frequency of the capture session (in Hz)."""
        return self._capture_freq_hz

    @capture_freq_hz.setter
    def capture_freq_hz(self, capture_frequency: float) -> None:
        """Set the capture frequency of the capture session (in Hz)."""
        if capture_frequency <= 0:
            raise ValueError('Capture frequency must be a positive number.')
        self._capture_freq_hz = capture_frequency

    @property
    def map(self) -> str:
        """Get the map name for the capture session."""
        return self._map

    @map.setter
    def map(self, map_name: str) -> None:
        """Set the map name for the capture session."""
        self._map = map_name

    @property
    def vehicle(self) -> VehicleConfig:
        """Get the vehicle configuration for the capture session."""
        return self._vehicle

    @vehicle.setter
    def vehicle(self, vehicle: VehicleConfig) -> None:
        """Set the vehicle configuration for the capture session."""
        self._vehicle = vehicle

    @property
    def cameras(self) -> List[CameraSensorConfig]:
        """Get the camera configurations for the capture session."""
        return self._cameras

    @cameras.setter
    def cameras(self, cameras: List[CameraSensorConfig]) -> None:
        """Set the camera configurations for the capture session."""
        self._cameras = cameras

    @property
    def weather(self) -> str:
        """Get the weather condition for the capture session."""
        return self._weather

    @weather.setter
    def weather(self, weather: str) -> None:
        """Set the weather condition for the capture session."""
        self._weather = weather

    @property
    def time(self) -> str:
        """Get the starting time of day for the capture session."""
        return self._time

    @time.setter
    def time(self, time: str) -> None:
        """Set the starting time of day for the capture session."""
        if not utils.is_hhmmss_time_string(time):
            raise ValueError('Time of day must be specified in the "HH:mm:ss" format.')
        self._time = time

    @property
    def num_ai_traffic_vehicles(self) -> int:
        """Get the number of AI traffic vehicles for the capture session."""
        return self._num_ai_traffic_vehicles

    @num_ai_traffic_vehicles.setter
    def num_ai_traffic_vehicles(self, num: int) -> None:
        """Set the number of AI traffic vehicles for the capture session."""
        if num < 0:
            raise ValueError('Number of AI traffic vehicles must be a non-negative number.')
        self._num_ai_traffic_vehicles = num

    @property
    def starting_waypoint(self) -> str:
        """Get the starting waypoint for the capture session."""
        return self._starting_waypoint

    @starting_waypoint.setter
    def starting_waypoint(self, waypoint: str) -> None:
        """Set the starting waypoint for the capture session."""
        self._starting_waypoint = waypoint

    def to_dict(self) -> SessionConfigDict:
        """Convert this session configuration to a dictionary."""
        generated_dict = {
            'scenario': self._scenario,
            'duration_s': self._duration_s,
            'capture_freq_hz': self._capture_freq_hz,
            'map': self._map,
            'vehicle': self._vehicle.to_dict(),
            'cameras': [camera.to_dict() for camera in self._cameras],
            'weather': self._weather,
            'time': self._time,
            'num_ai_traffic_vehicles': self._num_ai_traffic_vehicles,
            'starting_waypoint': self._starting_waypoint
        }
        return generated_dict

    def from_dict(self, config_dict: SessionConfigDict) -> None:
        """Load a session configuration from a dictionary."""
        self._scenario = config_dict['scenario']
        self._duration_s = config_dict['duration_s']
        self._capture_freq_hz = config_dict['capture_freq_hz']
        self._map = config_dict['map']
        self._vehicle = VehicleConfig()
        self._vehicle.from_dict(config_dict['vehicle'])
        self._cameras = []
        for camera_dict in config_dict['cameras']:
            cam = CameraSensorConfig()
            cam.from_dict(camera_dict)
            self._cameras.append(cam)
        self._weather = config_dict['weather']
        self._time = config_dict['time']
        self._num_ai_traffic_vehicles = config_dict['num_ai_traffic_vehicles']
        self._starting_waypoint = config_dict['starting_waypoint']

    def extract_session_metadata(self) -> SessionConfigDict:
        """
        Extract session metadata from the provided configuration.
        
        Only includes fields relevant as training data (excludes scenario, map, and vehicle).
        """
        metadata = {
            'duration_s': self.duration_s,
            'capture_freq_hz': self.capture_freq_hz,
            'cameras': [camera.extract_camera_metadata() for camera in self.cameras],
            'weather': self.weather,
            'time': self.time,
            'num_ai_traffic_vehicles': self.num_ai_traffic_vehicles
        }
        return metadata
    
    def validate(self) -> None:
        """
        Validate the session configuration.

        Raises ValueError if any field is invalid.
        """
        try:
            # Scenario and map: not empty or whitespace
            if not self.scenario or not isinstance(self.scenario, str) or not self.scenario.strip():
                raise ValueError('Scenario name error: must be a non-empty string.')
            if not self.map or not isinstance(self.map, str) or not self.map.strip():
                raise ValueError('Map name error: must be a non-empty string.')
            # Duration and frequency: positive float
            if self.duration_s is None or not isinstance(self.duration_s, (float, int)) or float(self.duration_s) <= 0:
                raise ValueError('Duration error: must be a positive number.')
            if self.capture_freq_hz is None or not isinstance(self.capture_freq_hz, (float, int)) or float(self.capture_freq_hz) <= 0:
                raise ValueError('Capture frequency error: must be a positive number.')
            # Time string
            if not self.time or not utils.is_hhmmss_time_string(self.time):
                raise ValueError('Time of day error: must be specified in the "HH:mm:ss" format.')
            # AI traffic vehicles: non-negative int
            if self.num_ai_traffic_vehicles is None or not isinstance(self.num_ai_traffic_vehicles, int) or self.num_ai_traffic_vehicles < 0:
                raise ValueError('AI traffic vehicles error: must be a non-negative integer.')
            # Starting waypoint: must be string
            if not isinstance(self.starting_waypoint, str):
                raise ValueError('Starting waypoint error: must be a string.')
            # Vehicle config
            self.vehicle.validate()
            # Cameras: at least one
            if not self.cameras or not isinstance(self.cameras, list):
                raise ValueError("Camera config error: at least one camera must be configured.")
            # Camera name uniqueness (ignoring case and whitespace)
            camera_names = []
            for camera in self.cameras:
                name = camera.name.strip().lower()
                if not name:
                    raise ValueError("Camera name error: cannot be empty or whitespace.")
                camera_names.append(name)
            if len(set(camera_names)) != len(camera_names):
                # Find the duplicates to output in the error message
                from collections import Counter
                counter = Counter(camera_names)
                duplicates = [names for (names, amount) in counter.items() if amount > 1]
                raise ValueError(f"Camera name error: duplicate camera name(s) {duplicates}. Each camera must have a unique name (case-insensitive, ignoring whitespace).")
            # Validate each camera
            for camera in self.cameras:
                camera.validate()
        except ValueError as e:
            raise ValueError(f'Invalid session configuration: {e}')

def create_session_config() -> SessionConfig:
    """Create a default session configuration."""
    session_config = SessionConfig()
    logging_mgr.log_action('Created default session configuration.')
    return session_config

def create_session_config_from_dict(config_dict: SessionConfigDict) -> SessionConfig:
    """Create a session configuration from a dictionary."""
    session_config = SessionConfig()
    session_config.from_dict(config_dict)
    logging_mgr.log_action('Created session configuration from dictionary.')
    return session_config

def create_session_config_from_file(file_path: str) -> SessionConfig:
    """Create a session configuration from a file."""
    config_dict = utils.load_json_file(file_path)
    session_config = create_session_config_from_dict(config_dict)
    logging_mgr.log_action(f'Created session configuration from file "{file_path}".')
    return session_config
