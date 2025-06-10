from gui_api import (GuiApi, RadioButton, RadioGroup, FileInput, IntInput, FloatInput,
                     StrInput, Label, Button, Checkbox, Window, GridContainer, RadioOption)
from type_defs import Any, Callable, Int2, List, Optional

import tkinter as tk
from tkinter import messagebox, filedialog



# --- Window Implementation ---
class TkWindow(Window):
    def __init__(self, tk_win):
        self._tk_win = tk_win
    def get(self):
        return self._tk_win
    def destroy(self) -> None:
        self._tk_win.destroy()
    def __setattr__(self, name, value):
        if name == '_tk_win':
            super().__setattr__(name, value)
        else:
            setattr(self._tk_win, name, value)
    def __getattr__(self, name):
        return getattr(self._tk_win, name)

class TkSubWindow(Window):
    def __init__(self, tk_win):
        self._tk_win = tk_win
    def get(self):
        return self._tk_win
    def destroy(self) -> None:
        self._tk_win.destroy()
    def __setattr__(self, name, value):
        if name == '_tk_win':
            super().__setattr__(name, value)
        else:
            setattr(self._tk_win, name, value)
    def __getattr__(self, name):
        return getattr(self._tk_win, name)

class TkGridContainer(GridContainer):
    def __init__(self, frame: tk.Frame, rows: int, columns: int, row_weights: list, column_weights: list):
        self.frame = frame
        # Configure row/column weights
        for i, w in enumerate(row_weights):
            self.frame.rowconfigure(i, weight=w)
        for j, w in enumerate(column_weights):
            self.frame.columnconfigure(j, weight=w)
    def get(self):
        return self.frame
    def destroy(self):
        self.frame.destroy()

# --- Widget Implementations ---
class TkRadioButton(RadioButton):
    """Tkinter implementation of a radio button."""
    def __init__(self, widget: tk.Radiobutton):
        """Initialize a TkRadioButton with a Tkinter Radiobutton widget."""
        self.widget = widget
    def get(self) -> str:
        """Get the value of the associated variable."""
        return self.widget.cget('value')
    def destroy(self) -> None:
        """Destroy the radio button widget."""
        self.widget.destroy()

class TkRadioGroup(RadioGroup):
    """Tkinter implementation of a radio group."""
    def __init__(self, frame, variable: tk.StringVar = None):
        """Initialize a TkRadioGroup with an optional StringVar."""
        if variable is None:
            variable = tk.StringVar()
        self.frame = frame
        self.variable = variable
        self.buttons = []

    def add_button(self, button: TkRadioButton) -> None:
        """Add a radio button to the group."""
        self.buttons.append(button)
        button.widget.config(variable=self.variable)
        button.widget.pack(anchor="w", in_=self.frame)

    def set_buttons(self, buttons: List[TkRadioButton]) -> None:
        """Set the list of radio buttons for this group, first is default."""
        self.buttons.clear()
        for idx, button in enumerate(buttons):
            self.add_button(button)
            if idx == 0:
                self.set_default(button.widget.cget('value'))

    def get(self) -> str:
        """Get the currently selected value."""
        return self.variable.get()

    def set_default(self, value: str) -> None:
        """Set the default (selected) value for the radio group."""
        self.variable.set(value)

    def destroy(self) -> None:
        """Destroy all radio buttons in the group."""
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()
        self.frame.destroy()

class TkFileInput(FileInput):
    """Tkinter implementation of a file input."""
    def __init__(self, var: tk.StringVar, entry_widget: tk.Entry = None):
        """Initialize a TkFileInput with a StringVar and optional Entry widget."""
        self.var = var
        self.entry_widget = entry_widget
    def get(self) -> str:
        """Get the current value of the file input."""
        return self.var.get()
    def destroy(self) -> None:
        """Destroy the entry widget if present."""
        if self.entry_widget is not None:
            self.entry_widget.destroy()

class TkIntInput(IntInput):
    """Tkinter implementation of an integer input."""
    def __init__(self, var: tk.StringVar, entry_widget: tk.Entry = None):
        """Initialize a TkIntInput with a StringVar and optional Entry widget."""
        self.var = var
        self.entry_widget = entry_widget
    def get(self) -> int:
        """Get the integer value from the input, or None if invalid."""
        try:
            return int(self.var.get())
        except Exception:
            return None
    def destroy(self) -> None:
        """Destroy the entry widget if present."""
        if self.entry_widget is not None:
            self.entry_widget.destroy()

class TkFloatInput(FloatInput):
    """Tkinter implementation of a float input."""
    def __init__(self, var: tk.StringVar, entry_widget: tk.Entry = None):
        """Initialize a TkFloatInput with a StringVar and optional Entry widget."""
        self.var = var
        self.entry_widget = entry_widget
    def get(self) -> float:
        """Get the float value from the input, or None if invalid."""
        try:
            return float(self.var.get())
        except Exception:
            return None
    def destroy(self) -> None:
        """Destroy the entry widget if present."""
        if self.entry_widget is not None:
            self.entry_widget.destroy()

class TkStrInput(StrInput):
    """Tkinter implementation of a string input."""
    def __init__(self, var: tk.StringVar, entry_widget: tk.Entry = None):
        """Initialize a TkStrInput with a StringVar and optional Entry widget."""
        self.var = var
        self.entry_widget = entry_widget
    def get(self) -> str:
        """Get the string value from the input."""
        return self.var.get()
    def destroy(self) -> None:
        """Destroy the entry widget if present."""
        if self.entry_widget is not None:
            self.entry_widget.destroy()

class TkLabel(Label):
    """Tkinter implementation of a label."""
    def __init__(self, widget: tk.Label):
        """Initialize a TkLabel with a Tkinter Label widget."""
        self.widget = widget
    def get(self) -> None:
        """Labels do not have a value."""
        return None
    def destroy(self) -> None:
        """Destroy the label widget."""
        self.widget.destroy()

class TkButton(Button):
    """Tkinter implementation of a button."""
    def __init__(self, widget: tk.Button):
        """Initialize a TkButton with a Tkinter Button widget."""
        self.widget = widget
    def get(self) -> None:
        """Buttons do not have a value."""
        return None
    def destroy(self) -> None:
        """Destroy the button widget."""
        self.widget.destroy()

class TkCheckbox(Checkbox):
    """Tkinter implementation of a checkbox."""
    def __init__(self, var: tk.BooleanVar, widget: tk.Checkbutton = None):
        """Initialize a TkCheckbox with a BooleanVar and optional Checkbutton widget."""
        self.var = var
        self.widget = widget
    def get(self) -> bool:
        """Get the boolean value of the checkbox."""
        return self.var.get()
    def destroy(self) -> None:
        """Destroy the checkbox widget if present."""
        if self.widget is not None:
            self.widget.destroy()

# --- API Implementation ---
class TkinterGuiApi(GuiApi):
    """
    Description:
    Implementation of the GuiApi interface using Tkinter. Provides functions to create and manage
    GUI elements for session configuration and user interaction.
    """

    def add_label(self, parent, text, font=None, pady=0, *, row=None, column=None, rowspan=1, columnspan=1):
        label = tk.Label(parent.get(), text=text, font=font)
        if isinstance(parent, TkGridContainer) and row is not None and column is not None:
            label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew", pady=pady)
        else:
            label.pack(pady=pady)
        return TkLabel(label)

    def add_radio_group(self, parent, label, *, row=None, column=None, rowspan=1, columnspan=1):
        group_frame = tk.Frame(parent.get())
        if isinstance(parent, TkGridContainer) and row is not None and column is not None:
            group_frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew")
        else:
            group_frame.pack(anchor="w", padx=20)
        tk.Label(group_frame, text=label).pack(anchor="w")
        group = TkRadioGroup(group_frame)
        return group

    def add_radio_button(self, parent, text, variable, value, group=None, *, row=None, column=None, rowspan=1, columnspan=1):
        rb = tk.Radiobutton(parent.get(), text=text, variable=variable, value=value)
        if isinstance(parent, TkGridContainer) and row is not None and column is not None:
            rb.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="w")
        else:
            rb.pack(anchor="w")
        radio_btn = TkRadioButton(rb)
        if group is not None:
            group.add_button(radio_btn)
        return radio_btn

    def add_file_input(self, parent, label, *, row=None, column=None, rowspan=1, columnspan=1):
        frame = tk.Frame(parent.get())
        if isinstance(parent, TkGridContainer) and row is not None and column is not None:
            frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew")
        else:
            frame.pack(anchor="w", padx=20)
        var = tk.StringVar()
        tk.Label(frame, text=label).pack(side="left")
        tk.Entry(frame, textvariable=var, width=30).pack(side="left")
        tk.Button(frame, text="Browse", command=lambda: var.set(filedialog.askopenfilename())).pack(side="left")
        return TkFileInput(var)

    def add_int_input(self, parent, label, default=0, *, row=None, column=None, rowspan=1, columnspan=1):
        var = tk.StringVar(value=str(default))
        label_widget = tk.Label(parent.get(), text=label)
        entry_widget = tk.Entry(parent.get(), textvariable=var)
        if isinstance(parent, TkGridContainer) and row is not None and column is not None:
            label_widget.grid(row=row, column=column, sticky="w")
            entry_widget.grid(row=row, column=column+1, sticky="w")
        else:
            label_widget.pack(anchor="w", padx=20)
            entry_widget.pack(anchor="w", padx=20)
        return TkIntInput(var)

    def add_float_input(self, parent, label, default=0.0, *, row=None, column=None, rowspan=1, columnspan=1):
        var = tk.StringVar(value=str(default))
        label_widget = tk.Label(parent.get(), text=label)
        entry_widget = tk.Entry(parent.get(), textvariable=var)
        if isinstance(parent, TkGridContainer) and row is not None and column is not None:
            label_widget.grid(row=row, column=column, sticky="w")
            entry_widget.grid(row=row, column=column+1, sticky="w")
        else:
            label_widget.pack(anchor="w", padx=20)
            entry_widget.pack(anchor="w", padx=20)
        return TkFloatInput(var)

    def add_str_input(self, parent, label, default="", *, row=None, column=None, rowspan=1, columnspan=1):
        var = tk.StringVar(value=default)
        label_widget = tk.Label(parent.get(), text=label)
        entry_widget = tk.Entry(parent.get(), textvariable=var)
        if isinstance(parent, TkGridContainer) and row is not None and column is not None:
            label_widget.grid(row=row, column=column, sticky="w")
            entry_widget.grid(row=row, column=column+1, sticky="w")
        else:
            label_widget.pack(anchor="w", padx=20)
            entry_widget.pack(anchor="w", padx=20)
        return TkStrInput(var)

    def add_button(self, parent, text, command, side="left", padx=0, pady=0, *, row=None, column=None, rowspan=1, columnspan=1):
        btn = tk.Button(parent.get(), text=text, command=command)
        if isinstance(parent, TkGridContainer) and row is not None and column is not None:
            btn.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew", padx=padx, pady=pady)
        else:
            btn.pack(side=side, padx=padx, pady=pady)
        return TkButton(btn)

    def add_checkbox(self, parent, label, default=False, *, row=None, column=None, rowspan=1, columnspan=1):
        var = tk.BooleanVar(value=default)
        cb = tk.Checkbutton(parent.get(), text=label, variable=var)
        if isinstance(parent, TkGridContainer) and row is not None and column is not None:
            cb.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="w")
        else:
            cb.pack(anchor="w", padx=20)
        return TkCheckbox(var)

    def create_window(self, title: str, size: Int2 = (400, 400)) -> TkWindow:
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{size[0]}x{size[1]}")
        return TkWindow(root)

    def create_subwindow(self, parent: Any, title: str, size: Int2 = (350, 400)) -> TkSubWindow:
        toplevel = tk.Toplevel(parent.get())
        toplevel.title(title)
        toplevel.geometry(f"{size[0]}x{size[1]}")
        return TkSubWindow(toplevel)

    def close_window(self, window: TkWindow) -> None:
        window.quit()
        window.destroy()

    def close_subwindow(self, subwindow: TkSubWindow) -> None:
        subwindow.destroy()

    def run_window(self, window: Window) -> None:
        window.mainloop()

    def wait_window(self, window: Window) -> None:
        window.wait_window()

    def show_error_message(self, message: str) -> None:
        tk.Tk().withdraw()
        messagebox.showerror("Error", message)

    def show_warning_message(self, message: str) -> None:
        tk.Tk().withdraw()
        messagebox.showwarning("Warning", message)
