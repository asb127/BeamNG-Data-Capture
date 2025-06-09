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

    window = _gui_api.create_window("BeamNG Data Capture - Session Setup", size=(400, 800))
    _gui_api.add_label(window, "BeamNG Data Capture - Session Setup", font=("Arial", 14), pady=10)

    # Session config fields
    session_source_rg = _gui_api.add_radio_group(window, "Session Source")
    _gui_api.add_label(window, "Session Configuration", font=("Arial", 12), pady=8)
    load_session_rb = _gui_api.add_radio_button(window, "Load session config from file", variable=session_source_rg.variable, value="load", group=session_source_rg)
    config_path_input = _gui_api.add_file_input(window, "Session config file:")
    create_session_rb = _gui_api.add_radio_button(window, "Create new session config", variable=session_source_rg.variable, value="new", group=session_source_rg)
    session_source_rg_buttons = [load_session_rb, create_session_rb]
    session_source_rg.set_buttons(session_source_rg_buttons)

    duration_input = _gui_api.add_int_input(window, "Duration (s):", default=settings.default_duration_s)
    freq_input = _gui_api.add_float_input(window, "Capture Freq (Hz):", default=settings.default_capture_freq_hz)
    weather_input = _gui_api.add_str_input(window, "Weather:", default=settings.default_weather)
    time_input = _gui_api.add_str_input(window, "Start Time (HH:mm:ss):", default=settings.time_of_day_start)
    num_ai_input = _gui_api.add_int_input(window, "AI Traffic Vehicles:", default=settings.default_num_ai_traffic_vehicles)

    # Vehicle config fields
    _gui_api.add_label(window, "Vehicle Configuration", font=("Arial", 12), pady=8)
    vehicle_name_input = _gui_api.add_str_input(window, "Vehicle Name:", default=settings.default_vehicle_name)
    vehicle_model_input = _gui_api.add_str_input(window, "Vehicle Model:", default=settings.default_vehicle_model)
    vehicle_pos_input = _gui_api.add_str_input(window, "Initial Position (x, y, z):", default="{}, {}, {}".format(*settings.default_vehicle_initial_position))
    vehicle_rot_input = _gui_api.add_str_input(window, "Initial Rotation (qx, qy, qz, qw):", default="{}, {}, {}, {}".format(*settings.default_vehicle_initial_rotation))

    # Camera sensor config fields (supports multiple entries)
    _gui_api.add_label(window, "Camera Sensor Configurations", font=("Arial", 12), pady=8)
    camera_widgets = []

    cameras_section = []

    def refresh_camera_list():
        # Remove previous camera labels/buttons from the window
        for widgets in cameras_section:
            for w in widgets:
                w.destroy()
        cameras_section.clear()

        for idx, (name_widget, pos_widget, res_widget, fov_widget, nearfar_widget, col_widget, ann_widget, dep_widget) in enumerate(camera_widgets):
            cam_name = name_widget.get()
            # Create a horizontal row for the camera name and its buttons
            row_widgets = []
            label = _gui_api.add_label(window, f"Camera: {cam_name}", font=("Arial", 10), pady=2)
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
                    cam_win.get().wait_window()
                return edit_camera
            def make_remove(idx=idx):
                def remove_camera():
                    del camera_widgets[idx]
                    logging_mgr.log_action(f"Removed camera config at index {idx} from GUI.")
                    refresh_camera_list()
                return remove_camera
            edit_btn = _gui_api.add_button(window, "Edit", make_edit(idx), side="left", padx=2, pady=2)
            remove_btn = _gui_api.add_button(window, "Remove", make_remove(idx), side="left", padx=2, pady=2)
            row_widgets.extend([edit_btn, remove_btn])
            cameras_section.append(row_widgets)

    def add_camera_row():
        cam_win = _gui_api.create_subwindow(window, "Add Camera Sensor", size=(350, 400))
        default_cam = CameraSensorConfig()
        name_widget = _gui_api.add_str_input(cam_win, "Camera Name:", default=default_cam.name)
        pos_widget = _gui_api.add_str_input(cam_win, "Position (x, y, z):", default=", ".join(map(str, default_cam.position)))
        res_widget = _gui_api.add_str_input(cam_win, "Resolution (w, h):", default=", ".join(map(str, default_cam.resolution)))
        fov_widget = _gui_api.add_int_input(cam_win, "FOV Y:", default=default_cam.fov_y)
        nearfar_widget = _gui_api.add_str_input(cam_win, "Near/Far Planes:", default=", ".join(map(str, default_cam.near_far_planes)))
        col_widget = _gui_api.add_checkbox(cam_win, "Render Colours", default=default_cam.is_render_colours)
        ann_widget = _gui_api.add_checkbox(cam_win, "Render Annotations", default=default_cam.is_render_annotations)
        dep_widget = _gui_api.add_checkbox(cam_win, "Render Depth", default=default_cam.is_render_depth)

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
                return  # Do not close the subwindow

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

    _gui_api.add_button(window, "Add Camera", on_add_camera, side="left", padx=10, pady=10)

    refresh_camera_list()

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

    _gui_api.add_button(window, "Start Capture", on_start, side="left", padx=20, pady=20)
    _gui_api.add_button(window, "Exit", on_exit, side="right", padx=20, pady=20)

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
