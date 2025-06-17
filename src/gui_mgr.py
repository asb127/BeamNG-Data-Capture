import os
import logging_mgr, session_config, settings, utils
from camera_sensor_config import CameraSensorConfig
from gui_api import GuiApi
from vehicle_config import VehicleConfig

# The GUI API instance should be injected or set externally for true independence.
_gui_api = None

_window_size = (700, 800)
_camera_subwindow_size = (400, 450)

_header_font = ("Arial", 10)
_label_font = ("Arial", 8)

def set_gui_api(api_instance: GuiApi) -> None:
    global _gui_api
    _gui_api = api_instance

def get_session_config():
    """
    Show the session configuration window, collect user input, and return a SessionConfig object.
    Implementation independent: uses only the abstract API interface.
    Returns None if the user cancels.
    """
    if _gui_api is None:
        raise RuntimeError("GUI API not set. Call set_gui_api() with an implementation before use.")

    window = _gui_api.create_window("BeamNG Data Capture - Session Setup", size=_window_size)
    num_rows = 25
    num_columns = 4
    grid = _gui_api.add_grid_container(window,
                                       num_rows=num_rows,
                                       num_columns=num_columns,
                                       row_weights=[1] * num_rows,
                                       column_weights=[1] * num_columns,
                                       padx=10,
                                       pady=10)

    # --- Session Source (one column, rows 0-3) ---
    session_source_rg = _gui_api.add_radio_group(grid,
                                                 row=0,
                                                 column=0,
                                                 columnspan=4)
    _gui_api.add_label(grid,
                       "Session Source",
                       font=_header_font,
                       row=0,
                       column=0,
                       columnspan=4,
                       fill=True)
    load_session_rb = _gui_api.add_radio_button(grid,
                                                "Load session config from file",
                                                variable=session_source_rg.variable,
                                                value="load",
                                                group=session_source_rg,
                                                row=1,
                                                column=0,
                                                columnspan=1)
    config_path_input = _gui_api.add_file_input(grid,
                                                "",
                                                row=1,
                                                column=1,
                                                columnspan=2)
    create_session_rb = _gui_api.add_radio_button(grid,
                                                  "Create new session config",
                                                  variable=session_source_rg.variable,
                                                  value="new",
                                                  group=session_source_rg,
                                                  row=2,
                                                  column=0,
                                                  columnspan=1)
    session_source_rg.set_buttons([load_session_rb, create_session_rb])

    # --- Session Config Fields (double columns, rows 3-8) ---
    _gui_api.add_label(grid,
                       "Session Configuration",
                       font=_header_font,
                       pady=8,
                       row=3,
                       column=0,
                       columnspan=4,
                       fill=True)
    # Row 1: Scenario | Map
    _gui_api.add_label(grid,
                       "Scenario name:",
                       font=_label_font,
                       row=4,
                       column=0)
    scenario_input = _gui_api.add_str_input(grid,
                                            default=settings.default_scenario,
                                            row=4,
                                            column=1)
    _gui_api.add_label(grid,
                       "Map:",
                       font=_label_font,
                       row=4,
                       column=2)
    map_input = _gui_api.add_str_input(grid,
                                       default=settings.default_map,
                                       row=4,
                                       column=3)
    # Row 2: Duration | Capture Frequency
    _gui_api.add_label(grid,
                       "Duration (s):",
                       font=_label_font,
                       row=5,
                       column=0)
    duration_input = _gui_api.add_float_input(grid,  # changed from add_int_input to add_float_input
                                              default=settings.default_duration_s,
                                              row=5,
                                              column=1)
    _gui_api.add_label(grid,
                       "Capture Frequency (Hz):",
                       font=_label_font,
                       row=5,
                       column=2)
    freq_input = _gui_api.add_float_input(grid,
                                          default=settings.default_capture_freq_hz,
                                          row=5,
                                          column=3)
    # Row 3: Weather | Start time
    _gui_api.add_label(grid,
                       "Weather:",
                       font=_label_font,
                       row=6,
                       column=0)
    weather_input = _gui_api.add_str_input(grid,
                                           default=settings.default_weather,
                                           row=6,
                                           column=1)
    _gui_api.add_label(grid,
                       "Start Time (HH:mm:ss):",
                       font=_label_font,
                       row=6,
                       column=2)
    time_input = _gui_api.add_str_input(grid,
                                        default=settings.time_of_day_start,
                                        row=6,
                                        column=3)
    # Row 4: AI Traffic Vehicles | Starting Waypoint
    _gui_api.add_label(grid,
                       "AI Traffic Vehicles:",
                       font=_label_font,
                       row=7,
                       column=0)
    num_ai_input = _gui_api.add_int_input(grid,
                                          default=settings.default_num_ai_traffic_vehicles,
                                          row=7,
                                          column=1)
    _gui_api.add_label(grid,
                       "Starting Waypoint:",
                       font=_label_font,
                       row=7,
                       column=2)
    starting_waypoint_input = _gui_api.add_str_input(grid,
                                                     default="",
                                                     row=7,
                                                     column=3)

    # --- Vehicle Config Fields (double columns, rows 9-13) ---
    _gui_api.add_label(grid,
                       "Vehicle Configuration",
                       font=_header_font,
                       pady=8,
                       row=9,
                       column=0,
                       columnspan=4,
                       fill=True)
    # First column
    _gui_api.add_label(grid,
                       "Vehicle Name:",
                       font=_label_font,
                       row=10,
                       column=0)
    vehicle_name_input = _gui_api.add_str_input(grid,
                                                default=settings.default_vehicle_name,
                                                row=10,
                                                column=1)
    _gui_api.add_label(grid,
                       "Initial Position (m) (x, y, z):",
                       font=_label_font,
                       row=11,
                       column=0)
    vehicle_pos_input = _gui_api.add_str_input(grid,
                                               default=utils.tuple_to_str(settings.default_vehicle_initial_position),
                                               row=11,
                                               column=1)
    # Second column
    _gui_api.add_label(grid,
                       "Vehicle Model:",
                       font=_label_font,
                       row=10,
                       column=2)
    vehicle_model_input = _gui_api.add_str_input(grid,
                                                 default=settings.default_vehicle_model,
                                                 row=10,
                                                 column=3)
    _gui_api.add_label(grid,
                       "Initial Rotation (deg) (roll, pitch, yaw):",
                       font=_label_font,
                       row=11,
                       column=2)
    vehicle_rot_input = _gui_api.add_str_input(grid,
                                               default=utils.tuple_to_str(utils.quaternion_to_euler(settings.default_vehicle_initial_rotation)),
                                               row=11,
                                               column=3)

    # --- Camera Config Section ---
    _gui_api.add_label(grid,
                       "Camera Sensor Configurations",
                       font=_header_font,
                       pady=8,
                       row=13,
                       column=0,
                       columnspan=4,
                       fill=True)
    camera_widgets = []
    cameras_section = []

    # Track the first row available for camera configs (after all previous widgets)
    camera_start_row = 14

    session = None

    def validate_session_fields():
        """
        Validates all main session fields. Returns True if succesful, false otherwise.

        Raises:
            ValueError: if any field is invalid.
            TypeError: if any field has the wrong type.
        """
        # Scenario and map must not be empty
        if not scenario_input.get().strip():
            raise ValueError("Scenario name cannot be empty.")
        if not map_input.get().strip():
            raise ValueError("Map cannot be empty.")
        # Duration must be a positive float
        try:
            duration = duration_input.get()
        except TypeError as te:
            raise TypeError(f"Duration: {te}")
        except ValueError as ve:
            raise ValueError(f"Duration: {ve}")
        if duration <= 0:
            raise ValueError("Duration must be a positive number.")
        # Frequency must be positive float
        try:
            freq = freq_input.get()
        except TypeError as te:
            raise TypeError(f"Capture frequency: {te}")
        except ValueError as ve:
            raise ValueError(f"Capture frequency: {ve}")
        if freq <= 0:
            raise ValueError("Capture frequency must be a positive number.")
        # Weather and time can be empty, but if time is not empty, it must be valid
        t = time_input.get().strip()
        if t and not utils.is_hhmmss_time_string(t):
            raise ValueError("Start Time must be in HH:mm:ss format.")
        # Vehicle name & model must not be empty
        if not vehicle_name_input.get().strip():
            raise ValueError("Vehicle name cannot be empty.")
        if not vehicle_model_input.get().strip():
            raise ValueError("Vehicle model cannot be empty.")
        # Initial vehicle position & rotation must be valid Float 3 tuples
        try:
            utils.str_to_tuple(vehicle_pos_input.get(), float, 3)
        except ValueError:
            raise TypeError("Vehicle initial position must be three comma-separated numbers.")
        try:
            utils.str_to_tuple(vehicle_rot_input.get(), float, 3)
        except ValueError:
            raise TypeError("Vehicle initial rotation must be three comma-separated numbers.")
        # AI traffic vehicles value must be a non-negative integer
        try:
            n_ai = num_ai_input.get()
        except TypeError as te:
            raise TypeError(f"AI Traffic Vehicles: {te}")
        except ValueError as ve:
            raise ValueError(f"AI Traffic Vehicles: {ve}")
        if n_ai < 0:
            raise ValueError("AI Traffic Vehicles must be zero or positive.")
        # No need to check starting waypoint since it can be empty
        return True

    def on_start():
        nonlocal session
        mode = session_source_rg.get()
        if mode == "load":
            file_path = config_path_input.get()
            if not file_path or not os.path.isfile(file_path):
                show_error_message("Please select a valid session config file.")
                return
            session = session_config.create_session_config_from_file(file_path)
            logging_mgr.log_action(f"Loaded session config from file: {file_path}")
        else:
            try:
                validate_session_fields()
            except (ValueError, TypeError) as err:
                show_warning_message(str(err))
                logging_mgr.log_action(f"Validation failed: {err}")
                return
            try:
                vehicle_pos = utils.str_to_tuple(vehicle_pos_input.get(), float, 3)
                vehicle_rot = utils.euler_to_quaternion(utils.str_to_tuple(vehicle_rot_input.get(), float, 3))
                vehicle = VehicleConfig(
                    name=vehicle_name_input.get(),
                    model=vehicle_model_input.get(),
                    initial_position=vehicle_pos,
                    initial_rotation=vehicle_rot
                )
                vehicle.validate()
                cameras = []
                for (name_widget, pos_widget, dir_widget, upv_widget, res_widget, fov_widget, nearfar_widget, col_widget, ann_widget, dep_widget) in camera_widgets:
                    try:
                        cam_pos = utils.str_to_tuple(pos_widget.get(), float, 3)
                        cam_dir = utils.str_to_tuple(dir_widget.get(), float, 3)
                        cam_upv = utils.str_to_tuple(upv_widget.get(), float, 3)
                        cam_res = utils.str_to_tuple(res_widget.get(), int, 2)
                        cam_nf = utils.str_to_tuple(nearfar_widget.get(), float, 2)
                        cam = CameraSensorConfig(
                            name=name_widget.get(),
                            position=cam_pos,
                            direction=cam_dir,
                            up_vector=cam_upv,
                            resolution=cam_res,
                            fov_y=int(fov_widget.get()),
                            near_far_planes=cam_nf,
                            is_render_colours=col_widget.get(),
                            is_render_annotations=ann_widget.get(),
                            is_render_depth=dep_widget.get()
                        )
                        cam.validate()
                    except ValueError as ve:
                        show_warning_message(f"Invalid camera config: {ve}")
                        return
                    cameras.append(cam)
                session = session_config.SessionConfig(
                    scenario=scenario_input.get(),
                    duration_s=duration_input.get(),
                    capture_freq_hz=freq_input.get(),
                    map_name=map_input.get(),
                    vehicle=vehicle,
                    cameras=cameras,
                    weather=weather_input.get(),
                    time=time_input.get(),
                    num_ai_traffic_vehicles=num_ai_input.get(),
                    starting_waypoint=starting_waypoint_input.get()
                )
                logging_mgr.log_action("Created new session config from GUI input.")
            except ValueError as ve:
                msg = f"Invalid input in session config: {ve}"
                show_warning_message(msg)
                logging_mgr.log_action(msg)
                return
            except Exception as ex:
                # Only catch generic Exception as a last resort for unexpected errors.
                show_error_message(f"Unexpected error: {ex}")
                logging_mgr.log_error(f"Unexpected error in session config: {ex}")
                return
        _gui_api.close_window(window)

    def on_exit():
        _gui_api.close_window(window)
        logging_mgr.log_action("User exited the session setup window.")
        exit(0)

    # Ensure we have enough rows for camera configs
    max_cameras = num_rows - camera_start_row - 2
    if max_cameras <= 0:
        show_error_message("Not enough space to add cameras. Please increase the number of rows available.")
        return None

    # --- Camera Config Buttons (bottom, always last row) ---
    def place_final_buttons():
        last_row = num_rows - 1
        # Only show "Add Camera" if there is space for more cameras
        max_camera_rows = num_rows - camera_start_row - 2
        if len(camera_widgets) < max_camera_rows:
            _gui_api.add_button(grid,
                                "Add Camera",
                                on_add_camera,
                                side="left",
                                padx=10,
                                pady=10,
                                row=last_row,
                                column=0,
                                fill=True)
        # Always show Start/Exit
        _gui_api.add_button(grid,
                            "Start Capture",
                            on_start,
                            side="left",
                            padx=10,
                            pady=10,
                            row=last_row,
                            column=2,
                            fill=True)
        _gui_api.add_button(grid,
                            "Exit",
                            on_exit,
                            side="right",
                            padx=10,
                            pady=10,
                            row=last_row,
                            column=3,
                            fill=True)

    def refresh_camera_list():
        # Remove previous camera rows
        for widgets in cameras_section:
            for w in widgets:
                w.destroy()
        cameras_section.clear()

        start_row = camera_start_row
        last_row = num_rows - 2  # Reserve the last row for buttons
        max_camera_rows = last_row - start_row

        # Only allow adding up to max_camera_rows cameras
        if len(camera_widgets) > max_camera_rows:
            del camera_widgets[max_camera_rows:]

        if not camera_widgets:
            label = _gui_api.add_label(grid, "(No cameras added)", font=_label_font, row=start_row, column=0, columnspan=4, fill=True)
            cameras_section.append([label])
        else:
            for idx, (name_widget, pos_widget, dir_widget, upv_widget, res_widget, fov_widget, nearfar_widget, col_widget, ann_widget, dep_widget) in enumerate(camera_widgets):
                cam_name = name_widget.get()
                row_widgets = []
                label = _gui_api.add_label(grid, f"Camera: {cam_name}", font=_label_font, pady=2, row=start_row+idx, column=0)
                row_widgets.append(label)
                def make_edit(idx=idx):
                    def edit_camera():
                        cam_win = _gui_api.create_subwindow(window, "Edit Camera Sensor", size=_camera_subwindow_size)
                        # Use the actual CameraSensorConfig object for this camera
                        cam = CameraSensorConfig(
                            name=camera_widgets[idx][0].get(),
                            position=utils.str_to_tuple(camera_widgets[idx][1].get(), float, 3),
                            direction=utils.str_to_tuple(camera_widgets[idx][2].get(), float, 3),
                            up_vector=utils.str_to_tuple(camera_widgets[idx][3].get(), float, 3),
                            resolution=utils.str_to_tuple(camera_widgets[idx][4].get(), int, 2),
                            fov_y=int(camera_widgets[idx][5].get()),
                            near_far_planes=utils.str_to_tuple(camera_widgets[idx][6].get(), float, 2),
                            is_render_colours=camera_widgets[idx][7].get(),
                            is_render_annotations=camera_widgets[idx][8].get(),
                            is_render_depth=camera_widgets[idx][9].get(),
                        )
                        widgets = camera_input_widgets(cam_win, cam)
                        name_w, pos_w, dir_w, upv_w, res_w, fov_w, nearfar_w, col_w, ann_w, dep_w = widgets
                        def on_save_edit():
                            try:
                                cam_pos = utils.str_to_tuple(pos_w.get(), float, 3)
                                cam_dir = utils.str_to_tuple(dir_w.get(), float, 3)
                                cam_upv = utils.str_to_tuple(upv_w.get(), float, 3)
                                cam_res = utils.str_to_tuple(res_w.get(), int, 2)
                                cam_nf = utils.str_to_tuple(nearfar_w.get(), float, 2)
                                cam = CameraSensorConfig(
                                    name=name_w.get(),
                                    position=cam_pos,
                                    direction=cam_dir,
                                    up_vector=cam_upv,
                                    resolution=cam_res,
                                    fov_y=int(fov_w.get()),
                                    near_far_planes=cam_nf,
                                    is_render_colours=col_w.get(),
                                    is_render_annotations=ann_w.get(),
                                    is_render_depth=dep_w.get()
                                )
                                cam.validate()
                            except Exception as ve:
                                show_warning_message(f"Invalid camera config: {ve}")
                                return
                            camera_widgets[idx] = (name_w, pos_w, dir_w, upv_w, res_w, fov_w, nearfar_w, col_w, ann_w, dep_w)
                            logging_mgr.log_action(f"Edited camera config '{name_w.get()}' in GUI.")
                            _gui_api.close_subwindow(cam_win)
                            refresh_camera_list()
                        def on_cancel_edit():
                            _gui_api.close_subwindow(cam_win)
                        _gui_api.add_button(cam_win, "Save", on_save_edit, side="left", padx=10, pady=10)
                        _gui_api.add_button(cam_win, "Cancel", on_cancel_edit, side="right", padx=10, pady=10)
                        _gui_api.focus_on(name_w)
                        _gui_api.wait_window(cam_win)
                    return edit_camera
                def make_remove(idx=idx):
                    def remove_camera():
                        del camera_widgets[idx]
                        logging_mgr.log_action(f"Removed camera config at index {idx} from GUI.")
                        refresh_camera_list()
                    return remove_camera
                edit_btn = _gui_api.add_button(grid, "Edit", make_edit(idx), side="left", padx=2, pady=2, row=start_row+idx, column=1, fill=True)
                remove_btn = _gui_api.add_button(grid, "Remove", make_remove(idx), side="left", padx=2, pady=2, row=start_row+idx, column=2, fill=True)
                row_widgets.extend([edit_btn, remove_btn])
                cameras_section.append(row_widgets)
        # Always place the final buttons at the last row of the grid (bottom of window)
        place_final_buttons()

    def camera_input_widgets(parent, cam: CameraSensorConfig) -> tuple:
        """
        Helper to create camera input widgets for add/edit.
        Returns tuple of widgets in the same order.
        """
        grid = _gui_api.add_grid_container(parent, num_rows=10, num_columns=2,
                                           row_weights=[0]*10, column_weights=[1, 2],
                                           padx=20, pady=20)
        _gui_api.add_label(grid, "Camera Name:", row=0, column=0, padx=20, pady=5)
        name_widget = _gui_api.add_str_input(grid, default=cam.name, row=0, column=1, padx=20, pady=5)
        _gui_api.add_label(grid, "Position (m) (x, y, z):", row=1, column=0, padx=20, pady=5)
        pos_widget = _gui_api.add_str_input(grid, default=utils.tuple_to_str(cam.position), row=1, column=1, padx=20, pady=5)
        _gui_api.add_label(grid, "Direction (x, y, z):", row=2, column=0, padx=20, pady=5)
        dir_widget = _gui_api.add_str_input(grid, default=utils.tuple_to_str(getattr(cam, "direction", (0,0,1))), row=2, column=1, padx=20, pady=5)
        _gui_api.add_label(grid, "Up Vector (x, y, z):", row=3, column=0, padx=20, pady=5)
        upv_widget = _gui_api.add_str_input(grid, default=utils.tuple_to_str(getattr(cam, "up_vector", (0,1,0))), row=3, column=1, padx=20, pady=5)
        _gui_api.add_label(grid, "Resolution (px) (w, h):", row=4, column=0, padx=20, pady=5)
        res_widget = _gui_api.add_str_input(grid, default=utils.tuple_to_str(cam.resolution, "{}"), row=4, column=1, padx=20, pady=5)
        _gui_api.add_label(grid, "FOV Y (deg):", row=5, column=0, padx=20, pady=5)
        fov_widget = _gui_api.add_int_input(grid, default=cam.fov_y, row=5, column=1, padx=20, pady=5)
        _gui_api.add_label(grid, "Near/Far Planes (m):", row=6, column=0, padx=20, pady=5)
        nearfar_widget = _gui_api.add_str_input(grid, default=utils.tuple_to_str(cam.near_far_planes), row=6, column=1, padx=20, pady=5)
        _gui_api.add_label(grid, "Render Colours:", row=7, column=0, padx=20, pady=5)
        col_widget = _gui_api.add_checkbox(grid, default=cam.is_render_colours, row=7, column=1, padx=20, pady=5)
        _gui_api.add_label(grid, "Render Annotations:", row=8, column=0, padx=20, pady=5)
        ann_widget = _gui_api.add_checkbox(grid, default=cam.is_render_annotations, row=8, column=1, padx=20, pady=5)
        _gui_api.add_label(grid, "Render Depth:", row=9, column=0, padx=20, pady=5)
        dep_widget = _gui_api.add_checkbox(grid, default=cam.is_render_depth, row=9, column=1, padx=20, pady=5)
        return (name_widget, pos_widget, dir_widget, upv_widget, res_widget, fov_widget, nearfar_widget, col_widget, ann_widget, dep_widget)

    def add_camera_row():
        cam_win = _gui_api.create_subwindow(window, "Add Camera Sensor", size=_camera_subwindow_size)
        default_cam = CameraSensorConfig()
        widgets = camera_input_widgets(cam_win, default_cam)
        name_widget, pos_widget, dir_widget, upv_widget, res_widget, fov_widget, nearfar_widget, col_widget, ann_widget, dep_widget = widgets

        def on_save_camera():
            try:
                cam_pos = utils.str_to_tuple(pos_widget.get(), float, 3)
                cam_dir = utils.str_to_tuple(dir_widget.get(), float, 3)
                cam_upv = utils.str_to_tuple(upv_widget.get(), float, 3)
                cam_res = utils.str_to_tuple(res_widget.get(), int, 2)
                cam_nf = utils.str_to_tuple(nearfar_widget.get(), float, 2)
                cam = CameraSensorConfig(
                    name=name_widget.get(),
                    position=cam_pos,
                    direction=cam_dir,
                    up_vector=cam_upv,
                    resolution=cam_res,
                    fov_y=int(fov_widget.get()),
                    near_far_planes=cam_nf,
                    is_render_colours=col_widget.get(),
                    is_render_annotations=ann_widget.get(),
                    is_render_depth=dep_widget.get()
                )
                cam.validate()
            except ValueError as ve:
                show_warning_message(f"Invalid camera config: {ve}")
                return  # Do not close the subwindow to allow user to correct input

            camera_widgets.append(widgets)
            logging_mgr.log_action(f"Added camera config '{name_widget.get()}' to GUI.")
            _gui_api.close_subwindow(cam_win)
            refresh_camera_list()

        def on_cancel_camera():
            _gui_api.close_subwindow(cam_win)

        _gui_api.add_button(cam_win, "Save Camera", on_save_camera, side="left", padx=20, pady=20, ipadx=20, ipady=10)
        _gui_api.add_button(cam_win, "Cancel", on_cancel_camera, side="right", padx=20, pady=20, ipadx=20, ipady=10)
        _gui_api.focus_on(name_widget)
        _gui_api.wait_window(cam_win)

    def on_add_camera():
        # Prevent adding more cameras than fit in the UI
        last_row = num_rows - 2
        max_camera_rows = last_row - camera_start_row
        if len(camera_widgets) >= max_camera_rows:
            show_warning_message(f"Maximum number of cameras ({max_camera_rows}) reached.")
            return
        add_camera_row()
        logging_mgr.log_action("User added a new camera config row.")

    refresh_camera_list()
    # Focus on the first input field (scenario_input) in the main window
    _gui_api.focus_on(scenario_input)

    _gui_api.run_window(window)
    return session

def show_error_message(message: str) -> None:
    if _gui_api is None:
        raise RuntimeError("GUI API not set. Call set_gui_api() with an implementation before use.")
    _gui_api.show_error_message(message)

def show_warning_message(message: str) -> None:
    if _gui_api is None:
        raise RuntimeError("GUI API not set. Call set_gui_api() with an implementation before use.")
    _gui_api.show_warning_message(message)
def show_warning_message(message: str) -> None:
    if _gui_api is None:
        raise RuntimeError("GUI API not set. Call set_gui_api() with an implementation before use.")
    _gui_api.show_warning_message(message)
    if _gui_api is None:
        raise RuntimeError("GUI API not set. Call set_gui_api() with an implementation before use.")
    _gui_api.show_warning_message(message)
