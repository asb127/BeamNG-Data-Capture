from typing import TypedDict

import settings
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
                 initial_position: Float3 = (-720, 100, 119),
                 initial_rotation: Quat = (0, 0, 0.35, 0.90)):
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
        '''Set the name of the vehicle.'''
        self._name = name

    @property
    def model(self) -> str:
        '''Get the model of the vehicle.'''
        return self._model

    @model.setter
    def model(self, model: str) -> None:
        '''Set the model of the vehicle.'''
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
