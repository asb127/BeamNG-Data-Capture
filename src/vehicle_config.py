from typing import TypedDict

import logging_mgr, settings
from beamngpy.types import Float3, Quat

class VehicleConfigDict(TypedDict):
    name: str
    model: str
    initial_position: Float3
    initial_rotation: Quat

class VehicleConfig:
    '''
    Configuration class for a vehicle.
    '''
    def __init__(self,
                 name: str = settings.default_vehicle_name,
                 model: str = settings.default_vehicle_model,
                 initial_position: Float3 = settings.default_vehicle_initial_position,
                 initial_rotation: Quat = settings.default_vehicle_initial_rotation):
        '''
        Initialize a new vehicle configuration with the provided parameters.
        '''
        self._name = name
        self._model = model
        self._initial_position = initial_position
        self._initial_rotation = initial_rotation

    @property
    def name(self) -> str:
        '''Get the name of the vehicle.'''
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        '''
        Set the name of the vehicle.
        
        The name cannot be empty.
        '''
        if not name:
            raise ValueError('Vehicle name cannot be empty.')

    @property
    def model(self) -> str:
        '''Get the model of the vehicle.'''
        return self._model

    @model.setter
    def model(self, model: str) -> None:
        '''
        Set the model of the vehicle.
        
        If the provided model is not supported, a warning is logged and the default vehicle model is used.
        If the default vehicle model is not supported, a ValueError is raised.
        '''
        if not model or model not in settings.supported_models:
            if settings.default_vehicle_model in settings.supported_models:
                logging_mgr.log_warning(f'Vehicle model "{model}" is not supported. Using default vehicle model "{settings.default_vehicle_model}".')
                model = settings.default_vehicle_model
            else:
                raise ValueError(f'Default vehicle model "{settings.default_vehicle_model}" is not supported.')
        self._model = model

    @property
    def initial_position(self) -> Float3:
        '''Get the initial location of the vehicle (x, y, z).'''
        return self._initial_position

    @initial_position.setter
    def initial_position(self, location: Float3) -> None:
        '''Set the initial location of the vehicle (x, y, z).'''
        self._initial_position = location

    @property
    def initial_rotation(self) -> Quat:
        '''Get the initial rotation of the vehicle (quaternion).'''
        return self._initial_rotation

    @initial_rotation.setter
    def initial_rotation(self, rotation: Quat) -> None:
        '''Set the initial rotation of the vehicle (quaternion).'''
        self._initial_rotation = rotation

    def to_dict(self) -> VehicleConfigDict:
        '''Convert this vehicle configuration to a dictionary.'''
        return {
            'name': self._name,
            'model': self._model,
            'initial_position': self._initial_position,
            'initial_rotation': self._initial_rotation
        }

    def from_dict(self, config_dict: VehicleConfigDict) -> None:
        '''Load a vehicle configuration from a dictionary.'''
        self._name = config_dict['name']
        self._model = config_dict['model']
        self._initial_position = config_dict['initial_position']
        self._initial_rotation = config_dict['initial_rotation']

    def validate(self) -> None:
        '''Validate the vehicle configuration. Same restrictions as setters.'''
        # Validate the vehicle name
        if not self._name:
            raise ValueError('Vehicle name cannot be empty.')
        # Validate the vehicle model
        if not self._model or self._model not in settings.supported_models:
            raise ValueError(f'Vehicle model "{self._model}" is not supported.')