from typing import TypedDict

from custom_types import Float3, Dimensions2D

class CameraSensorConfigDict(TypedDict):
    name: str
    position: Float3
    resolution: Dimensions2D
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
                 name: str = 'sensor_camera',
                 position: Float3 = (0, -0.5, 1.5),
                 resolution: Dimensions2D = (1280, 720),
                 is_render_colours: bool = True,
                 is_render_annotations: bool = True,
                 is_render_depth: bool = True,
                 fov_y: int = 70,
                 near_far_planes: tuple = (0.1, 1000.0)):
        '''
        Initialize a new camera sensor configuration with the provided parameters.
        '''
        self._name = name
        self._position = position
        self._resolution = resolution
        self._is_render_colours = is_render_colours
        self._is_render_annotations = is_render_annotations
        self._is_render_depth = is_render_depth
        self._fov_y = fov_y
        self._near_far_planes = near_far_planes

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
    def resolution(self) -> Dimensions2D:
        '''Get the resolution of the camera sensor (width, height).'''
        return self._resolution

    @resolution.setter
    def resolution(self, resolution: Dimensions2D) -> None:
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

    def extract_camera_metadata(self) -> dict:
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