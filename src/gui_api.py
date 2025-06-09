from abc import ABC, abstractmethod

from typing import Any, Callable, List, Optional
from beamngpy.types import Int2

# --- Container Interfaces ---
class Container(ABC):
    '''Base class for any widget container (Window or GridContainer).'''
    @abstractmethod
    def get(self) -> Any:
        '''Return the value of the container, if applicable.'''
        raise NotImplementedError()
    @abstractmethod
    def destroy(self) -> None:
        '''Destroy or remove the container from the GUI.'''
        raise NotImplementedError()

class Window(Container):
    '''Window interface.'''

class GridContainer(Container):
    '''Grid container interface.'''

# --- Widget Interfaces ---
class GuiWidget(ABC):
    @abstractmethod
    def get(self) -> Any:
        '''Return the value of the widget.'''
        raise NotImplementedError()

    @abstractmethod
    def destroy(self) -> None:
        '''Destroy or remove the widget from the GUI.'''
        raise NotImplementedError()

class RadioButton(GuiWidget):
    '''Radio button widget interface.'''

class RadioGroup(GuiWidget):
    '''Radio group widget interface.'''
    @abstractmethod
    def set_default(self, value: str) -> None:
        '''Set the default (selected) value for the radio group.'''
        raise NotImplementedError()
    @abstractmethod
    def add_button(self, button: RadioButton) -> None:
        '''Add an already-created radio button to the group.'''
        raise NotImplementedError()
    @abstractmethod
    def set_buttons(self, buttons: List[RadioButton]) -> None:
        '''Set the list of radio buttons for this group, first is default.'''
        raise NotImplementedError()

class FileInput(GuiWidget):
    '''File input widget interface.'''

class IntInput(GuiWidget):
    '''Integer input widget interface.'''

class FloatInput(GuiWidget):
    '''Float input widget interface.'''

class StrInput(GuiWidget):
    '''String input widget interface.'''

class Label(GuiWidget):
    '''Label widget interface.'''

class Button(GuiWidget):
    '''Button widget interface.'''

class Checkbox(GuiWidget):
    '''Checkbox widget interface.'''

class RadioOption:
    '''Strict definition for radio button options.'''
    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value

# --- API Interface ---
class GuiApi(ABC):
    @abstractmethod
    def create_window(self, title: str, size: tuple = (400, 400)) -> Window:
        '''Create and return a main window object.'''
        raise NotImplementedError()

    @abstractmethod
    def create_subwindow(self, parent: Container, title: str, size: Int2 = (350, 400)) -> Window:
        '''Create and return a subwindow (modal/subwindows) object.'''
        raise NotImplementedError()

    @abstractmethod
    def close_window(self, window: Window) -> None:
        '''Close and destroy the main/root window object.'''
        raise NotImplementedError()

    @abstractmethod
    def close_subwindow(self, subwindow: Window) -> None:
        '''Close and destroy a subwindow (modal/subwindows) object.'''
        raise NotImplementedError()

    @abstractmethod
    def run_window(self, window: Window) -> None:
        '''Run the window's main loop (for main/root windows).'''
        raise NotImplementedError()

    @abstractmethod
    def wait_window(self, window: Window) -> None:
        '''
        Block until the given window is closed (for modal/subwindows).
        '''
        raise NotImplementedError()

    @abstractmethod
    def add_label(self, parent: Container, text: str, font: Optional[Any] = None, pady: int = 0, *,
                  row: int = None, column: int = None, rowspan: int = 1, columnspan: int = 1) -> Label:
        '''Create a Label widget in the provided window and return it.'''
        raise NotImplementedError()

    @abstractmethod
    def add_radio_group(self, parent: Container, label: str, *,
                        row: int = None, column: int = None, rowspan: int = 1, columnspan: int = 1) -> RadioGroup:
        '''
        Add a radio group container to the parent.
        Radio buttons must be created separately and added to the group using add_button.
        '''
        raise NotImplementedError()

    @abstractmethod
    def add_radio_button(self, parent: Container, text: str, variable: Any, value: str, group: RadioGroup = None, *,
                         row: int = None, column: int = None, rowspan: int = 1, columnspan: int = 1) -> RadioButton:
        '''
        Create a single radio button in the provided window, sharing a variable with others.
        If a RadioGroup is provided, the button is registered with it.
        '''
        raise NotImplementedError()

    @abstractmethod
    def add_file_input(self, parent: Container, label: str, *,
                       row: int = None, column: int = None, rowspan: int = 1, columnspan: int = 1) -> FileInput:
        '''Create a FileInput widget in the provided window and return it.'''
        raise NotImplementedError()

    @abstractmethod
    def add_int_input(self, parent: Container, label: str, default: int = 0, *,
                      row: int = None, column: int = None, rowspan: int = 1, columnspan: int = 1) -> IntInput:
        '''Create a IntInput widget in the provided window and return it.'''
        raise NotImplementedError()

    @abstractmethod
    def add_float_input(self, parent: Container, label: str, default: float = 0.0, *,
                        row: int = None, column: int = None, rowspan: int = 1, columnspan: int = 1) -> FloatInput:
        '''Create a FloatInput widget in the provided window and return it.'''
        raise NotImplementedError()

    @abstractmethod
    def add_str_input(self, parent: Container, label: str, default: str = "", *,
                      row: int = None, column: int = None, rowspan: int = 1, columnspan: int = 1) -> StrInput:
        '''Create a StrInput widget in the provided window and return it.'''
        raise NotImplementedError()

    @abstractmethod
    def add_button(self, parent: Container, text: str, command: Callable[[], None], side: str = "left", padx: int = 0, pady: int = 0, *,
                   row: int = None, column: int = None, rowspan: int = 1, columnspan: int = 1) -> Button:
        '''Create a Button widget in the provided window and return it.'''
        raise NotImplementedError()

    @abstractmethod
    def add_checkbox(self, parent: Container, label: str, default: bool = False, *,
                     row: int = None, column: int = None, rowspan: int = 1, columnspan: int = 1) -> Checkbox:
        '''Create a Checkbox widget in the provided window and return it.'''
        raise NotImplementedError()

    @abstractmethod
    def show_error_message(self, message: str) -> None:
        '''Show an error message to the user.'''
        raise NotImplementedError()

    @abstractmethod
    def show_warning_message(self, message: str) -> None:
        '''Show a warning message to the user.'''
        raise NotImplementedError()

    @abstractmethod
    def create_subwindow(self, parent: Any, title: str, size: tuple = (350, 400)) -> Window:
        '''Create and return a subwindow (child window) object.'''
        raise NotImplementedError()
