from typing import TypedDict

from beamngpy.types import Float3, Int2, StrDict

class CameraSensorConfigDict(TypedDict):
    name: str
    position: Float3
    resolution: Int2
    is_render_colours: bool
    is_render_annotations: bool
    is_render_depth: bool
    fov_y: int
    near_far_planes: tuple

class CameraSensorConfig:
    '''
    Configuration class for a camera sensor.
    '''
    def __init__(self,
                 name: str = None,
                 position: Float3 = None,
                 resolution: Int2 = None,
                 is_render_colours: bool = None,
                 is_render_annotations: bool = None,
                 is_render_depth: bool = None,
                 fov_y: int = None,
                 near_far_planes: tuple = None):
        '''
        Initialize a new camera sensor configuration with the provided parameters.
        '''
        import settings
        self._name = name if name is not None else settings.default_camera_name
        self._position = position if position is not None else settings.default_camera_position
        self._resolution = resolution if resolution is not None else settings.default_camera_resolution
        self._is_render_colours = is_render_colours if is_render_colours is not None else settings.default_camera_render_flags['colour']
        self._is_render_annotations = is_render_annotations if is_render_annotations is not None else settings.default_camera_render_flags['annotation']
        self._is_render_depth = is_render_depth if is_render_depth is not None else settings.default_camera_render_flags['depth']
        self._fov_y = fov_y if fov_y is not None else settings.default_camera_fov_y
        self._near_far_planes = near_far_planes if near_far_planes is not None else settings.default_camera_near_far_planes

    @property
    def name(self) -> str:
        '''Get the name of the camera sensor.'''
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        '''Set the name of the camera sensor.'''
        self._name = name

    @property
    def position(self) -> Float3:
        '''Get the position of the camera sensor (x, y, z).'''
        return self._position

    @position.setter
    def position(self, position: Float3) -> None:
        '''Set the position of the camera sensor (x, y, z).'''
        self._position = position

    @property
    def resolution(self) -> Int2:
        '''Get the resolution of the camera sensor (width, height).'''
        return self._resolution

    @resolution.setter
    def resolution(self, resolution: Int2) -> None:
        '''Set the resolution of the camera sensor (width, height).'''
        self._resolution = resolution

    @property
    def is_render_colours(self) -> bool:
        '''Get the render colours flag of the camera sensor.'''
        return self._is_render_colours

    @is_render_colours.setter
    def is_render_colours(self, is_render_colours: bool) -> None:
        '''Set the render colours flag of the camera sensor.'''
        self._is_render_colours = is_render_colours

    @property
    def is_render_annotations(self) -> bool:
        '''Get the render annotations flag of the camera sensor.'''
        return self._is_render_annotations

    @is_render_annotations.setter
    def is_render_annotations(self, is_render_annotations: bool) -> None:
        '''Set the render annotations flag of the camera sensor.'''
        self._is_render_annotations = is_render_annotations

    @property
    def is_render_depth(self) -> bool:
        '''Get the render depth flag of the camera sensor.'''
        return self._is_render_depth

    @is_render_depth.setter
    def is_render_depth(self, is_render_depth: bool) -> None:
        '''Set the render depth flag of the camera sensor.'''
        self._is_render_depth = is_render_depth

    @property
    def fov_y(self) -> int:
        '''Get the field of view (Y) of the camera sensor.'''
        return self._fov_y

    @fov_y.setter
    def fov_y(self, fov_y: int) -> None:
        '''Set the field of view (Y) of the camera sensor.'''
        self._fov_y = fov_y

    @property
    def near_far_planes(self) -> tuple:
        '''Get the near and far planes of the camera sensor.'''
        return self._near_far_planes

    @near_far_planes.setter
    def near_far_planes(self, near_far_planes: tuple) -> None:
        '''Set the near and far planes of the camera sensor.'''
        self._near_far_planes = near_far_planes

    def to_dict(self) -> CameraSensorConfigDict:
        '''Convert this camera sensor configuration to a dictionary.'''
        return {
            'name': self._name,
            'position': self._position,
            'resolution': self._resolution,
            'is_render_colours': self._is_render_colours,
            'is_render_annotations': self._is_render_annotations,
            'is_render_depth': self._is_render_depth,
            'fov_y': self._fov_y,
            'near_far_planes': self._near_far_planes
        }

    def from_dict(self, config_dict: CameraSensorConfigDict) -> None:
        '''Load a camera sensor configuration from a dictionary.'''
        self._name = config_dict['name']
        self._position = config_dict['position']
        self._resolution = config_dict['resolution']
        self._is_render_colours = config_dict['is_render_colours']
        self._is_render_annotations = config_dict['is_render_annotations']
        self._is_render_depth = config_dict['is_render_depth']
        self._fov_y = config_dict['fov_y']
        self._near_far_planes = config_dict['near_far_planes']

    def extract_camera_metadata(self) -> StrDict:
        '''
        Extract metadata from the camera sensor configuration.
        
        Only includes fields relevant as training data (excludes render flags).
        Note: Name is included to differentiate cameras.
        '''
        camera_metadata = {
            'name': self.name,
            'position': self.position,
            'resolution': self.resolution,
            'fov_y': self.fov_y,
            'near_far_planes': self.near_far_planes
        }
        return camera_metadata
    
    def validate(self) -> None:
        '''
        Validate the camera sensor configuration.
        '''
        # Currently no validation is performed
        pass