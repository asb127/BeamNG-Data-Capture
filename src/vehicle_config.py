import logging_mgr, utils
from type_defs import Float3, Quat, TypedDict

class VehicleConfigDict(TypedDict):
    name: str
    model: str
    initial_position: Float3
    initial_rotation: Quat

class VehicleConfig:
    """
    Configuration class for a vehicle.
    """
    def __init__(self,
                 name: str = None,
                 model: str = None,
                 initial_position: Float3 = None,
                 initial_rotation: Quat = None):
        """
        Initialize a new vehicle configuration with the provided parameters.
        """
        import settings 

        self._name = name if name is not None else settings.default_vehicle_name
        self._model = model if model is not None else settings.default_vehicle_model
        self._initial_position = initial_position if initial_position is not None else settings.default_vehicle_initial_position
        self._initial_rotation = initial_rotation if initial_rotation is not None else settings.default_vehicle_initial_rotation

    @property
    def name(self) -> str:
        """Get the name of the vehicle."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Set the name of the vehicle.
        
        The name cannot be empty.
        """
        if not name:
            raise ValueError('Vehicle name cannot be empty.')
        self._name = name

    @property
    def model(self) -> str:
        """Get the model of the vehicle."""
        return self._model

    @model.setter
    def model(self, model: str) -> None:
        """
        Set the model of the vehicle.
        
        If the provided model is not supported, a warning is logged and the default vehicle model is used.
        If the default vehicle model is not supported, a ValueError is raised.
        """
        import settings 

        if not model or model not in settings.supported_models:
            if settings.default_vehicle_model in settings.supported_models:
                logging_mgr.log_warning(f'Vehicle model "{model}" is not supported. Using default vehicle model "{settings.default_vehicle_model}".')
                model = settings.default_vehicle_model
            else:
                raise ValueError(f'Default vehicle model "{settings.default_vehicle_model}" is not supported.')
        self._model = model

    @property
    def initial_position(self) -> Float3:
        """Get the initial location of the vehicle (x, y, z)."""
        return self._initial_position

    @initial_position.setter
    def initial_position(self, location: Float3) -> None:
        """Set the initial location of the vehicle (x, y, z)."""
        self._initial_position = location

    @property
    def initial_rotation(self) -> Quat:
        """Get the initial rotation of the vehicle (quaternion)."""
        return self._initial_rotation

    @initial_rotation.setter
    def initial_rotation(self, rotation: Quat) -> None:
        """Set the initial rotation of the vehicle (quaternion)."""
        self._initial_rotation = rotation

    def to_dict(self) -> VehicleConfigDict:
        """Convert this vehicle configuration to a dictionary."""
        return {
            'name': self._name,
            'model': self._model,
            'initial_position': self._initial_position,
            'initial_rotation': self._initial_rotation
        }

    def from_dict(self, config_dict: VehicleConfigDict) -> None:
        """Load a vehicle configuration from a dictionary."""
        self._name = config_dict['name']
        self._model = config_dict['model']
        self._initial_position = config_dict['initial_position']
        self._initial_rotation = config_dict['initial_rotation']

    def validate(self):
        """
        Validate the vehicle configuration.

        Raises ValueError if any field is invalid.
        """
        # Check if all required fields are set and valid in size and type
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Vehicle name error: must be a non-empty string.")
        if not self.model or not isinstance(self.model, str):
            raise ValueError("Vehicle model error: must be a non-empty string.")
        if not isinstance(self.initial_position, tuple) or len(self.initial_position) != 3:
            raise ValueError("Initial position error: must be a tuple of 3 numbers.")
        if not isinstance(self.initial_rotation, tuple) or len(self.initial_rotation) != 4:
            raise ValueError("Initial rotation error: must be a tuple of 4 numbers (quaternion).")
        # Check if the initial position and rotation fields are finite number vectors
        if not utils.are_finite(self.initial_position):
            raise ValueError("Initial position error: values must be finite numbers.")
        if not utils.are_finite(self.initial_rotation):
            raise ValueError("Initial rotation error: values must be finite numbers.")
        # Check if the model is specified as supported in the settings
        if not self.model in utils.get_supported_vehicle_models():
            raise ValueError(f"Vehicle model error: '{self.model}' is not supported.")