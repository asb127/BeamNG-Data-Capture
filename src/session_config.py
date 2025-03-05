from typing import TypedDict, List

import logging_mgr, utils
from vehicle_config import VehicleConfig
from camera_sensor_config import CameraSensorConfig

class SessionConfigDict(TypedDict):
    scenario: str
    duration_s: int
    capture_freq_hz: float
    map: str
    vehicle: VehicleConfig
    cameras: List[CameraSensorConfig]
    weather: str
    num_ai_traffic_vehicles: int

class SessionConfig:
    '''
    Configuration class for a capture session.
    '''
    def __init__(self,
                 scenario: str = 'default_scenario',
                 duration_s: int = 10,
                 capture_freq_hz: float = 0.5,
                 map_name: str = 'west_coast_usa',
                 vehicle: VehicleConfig = VehicleConfig(),
                 cameras: List[CameraSensorConfig] = [CameraSensorConfig()],
                 weather: str = '',
                 num_ai_traffic_vehicles: int = 10):
        '''
        Initialize a new session configuration with the provided parameters.
        '''
        self._scenario = scenario
        self._duration_s = duration_s
        self._capture_freq_hz = capture_freq_hz
        self._map = map_name
        self._vehicle = vehicle
        self._cameras = cameras
        self._weather = weather
        self._num_ai_traffic_vehicles = num_ai_traffic_vehicles

    @property
    def scenario(self) -> str:
        '''Get the scenario name of the session configuration.'''
        return self._scenario

    @scenario.setter
    def scenario(self, scenario: str) -> None:
        '''Set the scenario name of the session configuration.'''
        self._scenario = scenario

    @property
    def duration_s(self) -> int:
        '''Get the duration of the capture session (in seconds).'''
        return self._duration_s

    @duration_s.setter
    def duration_s(self, duration: int) -> None:
        '''Set the duration of the capture session (in seconds).'''
        if duration <= 0:
            raise ValueError('Duration must be a positive number.')
        self._duration_s = duration

    @property
    def capture_freq_hz(self) -> float:
        '''Get the capture frequency of the capture session (in Hz).'''
        return self._capture_freq_hz

    @capture_freq_hz.setter
    def capture_freq_hz(self, capture_frequency: float) -> None:
        '''Set the capture frequency of the capture session (in Hz).'''
        if capture_frequency <= 0:
            raise ValueError('Capture frequency must be a positive number.')
        self._capture_freq_hz = capture_frequency

    @property
    def map(self) -> str:
        '''Get the map name for the capture session.'''
        return self._map

    @map.setter
    def map(self, map_name: str) -> None:
        '''Set the map name for the capture session.'''
        self._map = map_name

    @property
    def vehicle(self) -> VehicleConfig:
        '''Get the vehicle configuration for the capture session.'''
        return self._vehicle

    @vehicle.setter
    def vehicle(self, vehicle: VehicleConfig) -> None:
        '''Set the vehicle configuration for the capture session.'''
        self._vehicle = vehicle

    @property
    def cameras(self) -> List[CameraSensorConfig]:
        '''Get the camera configurations for the capture session.'''
        return self._cameras

    @cameras.setter
    def cameras(self, cameras: List[CameraSensorConfig]) -> None:
        '''Set the camera configurations for the capture session.'''
        self._cameras = cameras

    @property
    def weather(self) -> str:
        '''Get the weather condition for the capture session.'''
        return self._weather

    @weather.setter
    def weather(self, weather: str) -> None:
        '''Set the weather condition for the capture session.'''
        self._weather = weather

    @property
    def num_ai_traffic_vehicles(self) -> int:
        '''Get the number of AI traffic vehicles for the capture session.'''
        return self._num_ai_traffic_vehicles

    @num_ai_traffic_vehicles.setter
    def num_ai_traffic_vehicles(self, num: int) -> None:
        '''Set the number of AI traffic vehicles for the capture session.'''
        if num < 0:
            raise ValueError('Number of AI traffic vehicles must be a non-negative number.')
        self._num_ai_traffic_vehicles = num

    def to_dict(self) -> SessionConfigDict:
        '''Convert this session configuration to a dictionary.'''
        generated_dict = {
            'scenario': self._scenario,
            'duration_s': self._duration_s,
            'capture_freq_hz': self._capture_freq_hz,
            'map': self._map,
            'vehicle': self._vehicle.to_dict(),
            'cameras': [camera.to_dict() for camera in self._cameras],
            'weather': self._weather,
            'num_ai_traffic_vehicles': self._num_ai_traffic_vehicles
        }
        return generated_dict

    def from_dict(self, config_dict: SessionConfigDict) -> None:
        '''Load a session configuration from a dictionary.'''
        self._scenario = config_dict['scenario']
        self._duration_s = config_dict['duration_s']
        self._capture_freq_hz = config_dict['capture_freq_hz']
        self._map = config_dict['map']
        self._vehicle = VehicleConfig()
        self._vehicle.from_dict(config_dict['vehicle'])
        self._cameras = [CameraSensorConfig().from_dict(camera) for camera in config_dict['cameras']]
        self._weather = config_dict['weather']
        self._num_ai_traffic_vehicles = config_dict['num_ai_traffic_vehicles']

    def extract_session_metadata(self) -> SessionConfigDict:
        '''
        Extract session metadata from the provided configuration.
        
        Only includes fields relevant as training data (excludes scenario, map, and vehicle).
        '''
        metadata = {
            'duration_s': self.duration_s,
            'capture_freq_hz': self.capture_freq_hz,
            'cameras': [camera.extract_camera_metadata() for camera in self.cameras],
            'weather': self.weather,
            'num_ai_traffic_vehicles': self.num_ai_traffic_vehicles
        }
        return metadata
    
    def validate(self) -> None:
        '''Validate the session configuration.'''
        try:
            if self.duration_s <= 0:
                raise ValueError('Duration must be a positive number.')
            if self.capture_freq_hz <= 0:
                raise ValueError('Capture frequency must be a positive number.')
            if self.num_ai_traffic_vehicles < 0:
                raise ValueError('Number of AI traffic vehicles must be a non-negative number.')
            self.vehicle.validate()
            for camera in self.cameras:
                camera.validate()
        except ValueError as e:
            raise ValueError(f'Invalid session configuration: {e}')

def create_session_config() -> SessionConfig:
    '''Create a default session configuration.'''
    session_config = SessionConfig()
    logging_mgr.log_action('Created default session configuration.')
    return session_config

def create_session_config_from_dict(config_dict: SessionConfigDict) -> SessionConfig:
    '''Create a session configuration from a dictionary.'''
    session_config = SessionConfig()
    session_config.from_dict(config_dict)
    logging_mgr.log_action('Created session configuration from dictionary.')
    return session_config

def create_session_config_from_file(file_path: str) -> SessionConfig:
    '''Create a session configuration from a file.'''
    config_dict = utils.load_json_file(file_path)
    session_config = create_session_config_from_dict(config_dict)
    logging_mgr.log_action(f'Created session configuration from file "{file_path}".')
    return session_config
