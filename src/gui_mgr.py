import os
import logging_mgr, session_config, settings, utils
from camera_sensor_config import CameraSensorConfig
from gui_api import GuiApi
from vehicle_config import VehicleConfig

# The GUI API instance should be injected or set externally for true independence.
_gui_api = None

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

    window = _gui_api.create_window("BeamNG Data Capture - Session Setup", size=(600, 900))
    num_rows = 30
    num_columns = 4
    grid = _gui_api.add_grid_container(window,
                                       num_rows=num_rows,
                                       num_columns=num_columns,
                                       row_weights=[1] * num_rows,
                                       column_weights=[1] * num_columns,
                                       padx=10,
                                       pady=10)

    # --- Session Source (one column, rows 0-2) ---
    session_source_rg = _gui_api.add_radio_group(grid,
                                                 "Session Source",
                                                 row=0,
                                                 column=0,
                                                 columnspan=1)
    load_session_rb = _gui_api.add_radio_button(grid,
                                                "Load session config from file",
                                                variable=session_source_rg.variable,
                                                value="load",
                                                group=session_source_rg,
                                                row=1,
                                                column=0,
                                                columnspan=1)
    config_path_input = _gui_api.add_file_input(grid,
                                                "Session config file:",
                                                row=2,
                                                column=0,
                                                columnspan=1)
    create_session_rb = _gui_api.add_radio_button(grid,
                                                  "Create new session config",
                                                  variable=session_source_rg.variable,
                                                  value="new",
                                                  group=session_source_rg,
                                                  row=3,
                                                  column=0,
                                                  columnspan=1)
    session_source_rg.set_buttons([load_session_rb, create_session_rb])

    # --- Session Config Fields (two columns, rows 4-8) ---
    _gui_api.add_label(grid,
                       "Session Configuration",
                       font=("Arial", 12),
                       pady=8,
                       row=4,
                       column=0,
                       columnspan=2)
    _gui_api.add_label(grid,
                       "Duration (s):",
                       row=5,
                       column=0)
    duration_input = _gui_api.add_int_input(grid,
                                            default=settings.default_duration_s,
                                            row=5,
                                            column=1)
    _gui_api.add_label(grid,
                       "Capture Freq (Hz):",
                       row=6,
                       column=0)
    freq_input = _gui_api.add_float_input(grid,
                                          default=settings.default_capture_freq_hz,
                                          row=6,
                                          column=1)
    _gui_api.add_label(grid,
                       "Weather:",
                       row=7,
                       column=0)
    weather_input = _gui_api.add_str_input(grid,
                                           default=settings.default_weather,
                                           row=7,
                                           column=1)
    _gui_api.add_label(grid,
                       "Start Time (HH:mm:ss):",
                       row=8,
                       column=0)
    time_input = _gui_api.add_str_input(grid,
                                        default=settings.time_of_day_start,
                                        row=8,
                                        column=1)
    _gui_api.add_label(grid,
                       "AI Traffic Vehicles:",
                       row=9,
                       column=0)
    num_ai_input = _gui_api.add_int_input(grid,
                                          default=settings.default_num_ai_traffic_vehicles,
                                          row=9,
                                          column=1)

    # --- Vehicle Config Fields (two columns, rows 10-13, columns 0-1) ---
    _gui_api.add_label(grid,
                       "Vehicle Configuration",
                       font=("Arial", 12),
                       pady=8,
                       row=10,
                       column=0,
                       columnspan=2)
    _gui_api.add_label(grid,
                       "Vehicle Name:",
                       row=11,
                       column=0)
    vehicle_name_input = _gui_api.add_str_input(
        grid,
        default=settings.default_vehicle_name,
        row=11,
        column=1)
    _gui_api.add_label(grid,
                       "Vehicle Model:",
                       row=12,
                       column=0)
    vehicle_model_input = _gui_api.add_str_input(
        grid,
        default=settings.default_vehicle_model,
        row=12,
        column=1)
    _gui_api.add_label(grid,
                       "Initial Position (x, y, z):",
                       row=13,
                       column=0)
    vehicle_pos_input = _gui_api.add_str_input(
        grid,
        default="{}, {}, {}".format(*settings.default_vehicle_initial_position),
        row=13,
        column=1)
    _gui_api.add_label(grid,
                       "Initial Rotation (qx, qy, qz, qw):",
                       row=14,
                       column=0)
    vehicle_rot_input = _gui_api.add_str_input(
        grid,
        default="{}, {}, {}, {}".format(*settings.default_vehicle_initial_rotation),
        row=14,
        column=1)

    # --- Camera Config Section ---
    _gui_api.add_label(grid,
                       "Camera Sensor Configurations",
                       font=("Arial", 12),
                       pady=8,
                       row=15,
                       column=0,
                       columnspan=3)
    camera_widgets = []
    cameras_section = []

    # Track the first row available for camera configs (after all previous inputs)
    camera_start_row = 16

    session = None

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
                vehicle_pos = utils.tuple_from_str(vehicle_pos_input.get(), float, 3)
                vehicle_rot = utils.tuple_from_str(vehicle_rot_input.get(), float, 4)
                vehicle = VehicleConfig(
                    name=vehicle_name_input.get(),
                    model=vehicle_model_input.get(),
                    initial_position=vehicle_pos,
                    initial_rotation=vehicle_rot
                )
                cameras = []
                for (name_widget, pos_widget, res_widget, fov_widget, nearfar_widget, col_widget, ann_widget, dep_widget) in camera_widgets:
                    cam_pos = utils.tuple_from_str(pos_widget.get(), float, 3)
                    cam_res = utils.tuple_from_str(res_widget.get(), int, 2)
                    cam_nf = utils.tuple_from_str(nearfar_widget.get(), float, 2)
                    cam = CameraSensorConfig(
                        name=name_widget.get(),
                        position=cam_pos,
                        resolution=cam_res,
                        fov_y=int(fov_widget.get()),
                        near_far_planes=cam_nf,
                        is_render_colours=col_widget.get().lower() == "true",
                        is_render_annotations=ann_widget.get().lower() == "true",
                        is_render_depth=dep_widget.get().lower() == "true"
                    )
                    cameras.append(cam)
                session = session_config.SessionConfig(
                    duration_s=duration_input.get(),
                    capture_freq_hz=freq_input.get(),
                    weather=weather_input.get(),
                    time=time_input.get(),
                    num_ai_traffic_vehicles=num_ai_input.get(),
                    vehicle=vehicle,
                    cameras=cameras
                )
                logging_mgr.log_action("Created new session config from GUI input.")
            except ValueError as ve:
                msg = f"Invalid input in session config: {ve}"
                show_warning_message(msg)
                logging_mgr.log_action(msg)
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
        if len(camera_widgets) < max_cameras:
            _gui_api.add_button(grid,
                                "Add Camera",
                                on_add_camera,
                                side="left",
                                padx=10,
                                pady=10,
                                row=last_row,
                                column=0)
        # Always show Start/Exit
        _gui_api.add_button(grid,
                            "Start Capture",
                            on_start,
                            side="left",
                            padx=20,
                            pady=20,
                            row=last_row,
                            column=1)
        _gui_api.add_button(grid,
                            "Exit",
                            on_exit,
                            side="right",
                            padx=20,
                            pady=20,
                            row=last_row,
                            column=2)

    def refresh_camera_list():
        # Remove previous camera rows
        for widgets in cameras_section:
            for w in widgets:
                w.destroy()
        cameras_section.clear()

        start_row = camera_start_row
        if not camera_widgets:
            label = _gui_api.add_label(grid, "No cameras added", font=("Arial", 10), row=start_row, column=0, columnspan=3)
            cameras_section.append([label])
            next_row = start_row + 1
        else:
            for idx, (name_widget, pos_widget, res_widget, fov_widget, nearfar_widget, col_widget, ann_widget, dep_widget) in enumerate(camera_widgets):
                cam_name = name_widget.get()
                row_widgets = []
                label = _gui_api.add_label(grid, f"Camera: {cam_name}", font=("Arial", 10), pady=2, row=start_row+idx, column=0)
                row_widgets.append(label)
                def make_edit(idx=idx):
                    def edit_camera():
                        cam_win = _gui_api.create_subwindow(window, "Edit Camera Sensor", size=(350, 400))
                        name_w = _gui_api.add_str_input(cam_win, "Camera Name:", default=name_widget.get())
                        pos_w = _gui_api.add_str_input(cam_win, "Position (x, y, z):", default=pos_widget.get())
                        res_w = _gui_api.add_str_input(cam_win, "Resolution (w, h):", default=res_widget.get())
                        fov_w = _gui_api.add_int_input(cam_win, "FOV Y:", default=int(fov_widget.get()))
                        nearfar_w = _gui_api.add_str_input(cam_win, "Near/Far Planes:", default=nearfar_widget.get())
                        col_w = _gui_api.add_checkbox(cam_win, "Render Colours", default=col_widget.get())
                        ann_w = _gui_api.add_checkbox(cam_win, "Render Annotations", default=ann_widget.get())
                        dep_w = _gui_api.add_checkbox(cam_win, "Render Depth", default=dep_widget.get())
                        def on_save_edit():
                            try:
                                cam_pos = utils.tuple_from_str(pos_w.get(), float, 3)
                                cam_res = utils.tuple_from_str(res_w.get(), int, 2)
                                cam_nf = utils.tuple_from_str(nearfar_w.get(), float, 2)
                                cam = CameraSensorConfig(
                                    name=name_w.get(),
                                    position=cam_pos,
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
                            camera_widgets[idx] = (name_w, pos_w, res_w, fov_w, nearfar_w, col_w, ann_w, dep_w)
                            logging_mgr.log_action(f"Edited camera config '{name_w.get()}' in GUI.")
                            _gui_api.close_subwindow(cam_win)
                            refresh_camera_list()
                        def on_cancel_edit():
                            _gui_api.close_subwindow(cam_win)
                        _gui_api.add_button(cam_win, "Save", on_save_edit, side="left", padx=10, pady=10)
                        _gui_api.add_button(cam_win, "Cancel", on_cancel_edit, side="right", padx=10, pady=10)
                        _gui_api.wait_window(cam_win)
                    return edit_camera
                def make_remove(idx=idx):
                    def remove_camera():
                        del camera_widgets[idx]
                        logging_mgr.log_action(f"Removed camera config at index {idx} from GUI.")
                        refresh_camera_list()
                    return remove_camera
                edit_btn = _gui_api.add_button(grid, "Edit", make_edit(idx), side="left", padx=2, pady=2, row=start_row+idx, column=1)
                remove_btn = _gui_api.add_button(grid, "Remove", make_remove(idx), side="left", padx=2, pady=2, row=start_row+idx, column=2)
                row_widgets.extend([edit_btn, remove_btn])
                cameras_section.append(row_widgets)
            next_row = start_row + len(camera_widgets)
        # Always place the final buttons at the last row of the grid (bottom of window)
        place_final_buttons()

    def add_camera_row():
        cam_win = _gui_api.create_subwindow(window, "Add Camera Sensor", size=(350, 400))
        default_cam = CameraSensorConfig()
        _gui_api.add_label(cam_win, "Camera Name:", row=0, column=0)
        name_widget = _gui_api.add_str_input(cam_win, default=default_cam.name, row=0, column=1)
        _gui_api.add_label(cam_win, "Position (x, y, z):", row=1, column=0)
        pos_widget = _gui_api.add_str_input(cam_win, default=", ".join(map(str, default_cam.position)), row=1, column=1)
        _gui_api.add_label(cam_win, "Resolution (w, h):", row=2, column=0)
        res_widget = _gui_api.add_str_input(cam_win, default=", ".join(map(str, default_cam.resolution)), row=2, column=1)
        _gui_api.add_label(cam_win, "FOV Y:", row=3, column=0)
        fov_widget = _gui_api.add_int_input(cam_win, default=default_cam.fov_y, row=3, column=1)
        _gui_api.add_label(cam_win, "Near/Far Planes:", row=4, column=0)
        nearfar_widget = _gui_api.add_str_input(cam_win, default=", ".join(map(str, default_cam.near_far_planes)), row=4, column=1)
        _gui_api.add_label(cam_win, "Render Colours", row=5, column=0)
        col_widget = _gui_api.add_checkbox(cam_win, default=default_cam.is_render_colours, row=5, column=1)
        _gui_api.add_label(cam_win, "Render Annotations", row=6, column=0)
        ann_widget = _gui_api.add_checkbox(cam_win, default=default_cam.is_render_annotations, row=6, column=1)
        _gui_api.add_label(cam_win, "Render Depth", row=7, column=0)
        dep_widget = _gui_api.add_checkbox(cam_win, default=default_cam.is_render_depth, row=7, column=1)

        def on_save_camera():
            try:
                cam_pos = utils.tuple_from_str(pos_widget.get(), float, 3)
                cam_res = utils.tuple_from_str(res_widget.get(), int, 2)
                cam_nf = utils.tuple_from_str(nearfar_widget.get(), float, 2)
                cam = CameraSensorConfig(
                    name=name_widget.get(),
                    position=cam_pos,
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

            camera_widgets.append((name_widget, pos_widget, res_widget, fov_widget, nearfar_widget, col_widget, ann_widget, dep_widget))
            logging_mgr.log_action(f"Added camera config '{name_widget.get()}' to GUI.")
            _gui_api.close_subwindow(cam_win)
            refresh_camera_list()

        def on_cancel_camera():
            _gui_api.close_subwindow(cam_win)

        _gui_api.add_button(cam_win, "Save Camera", on_save_camera, side="left", padx=10, pady=10)
        _gui_api.add_button(cam_win, "Cancel", on_cancel_camera, side="right", padx=10, pady=10)
        _gui_api.wait_window(cam_win)

    def on_add_camera():
        add_camera_row()
        logging_mgr.log_action("User added a new camera config row.")

    refresh_camera_list()

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
