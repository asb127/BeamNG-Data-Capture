import os
from datetime import datetime
from beamngpy.sensors import Camera

import logging_mgr

def create_output_dir():
    # Create a directory to store the captured images
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = os.path.join(os.path.expanduser('~'),
                              'Documents',
                              'BeamNG-Data-Capture',
                              timestamp)
    os.makedirs(output_dir, exist_ok=True)
    logging_mgr.log_action(f'Output directory created at "{output_dir}".')
    return output_dir

def create_frame_output_dir(output_dir, i):
    # Create a subfolder for every frame
    frame_dir = os.path.join(output_dir, f'frame_{i}')
    os.makedirs(frame_dir, exist_ok=True)
    logging_mgr.log_action(f'Frame {i} output directory created at "{output_dir}".')
    return frame_dir

def create_camera_sensor(bng,
                         vehicle,
                         name,
                         pos,
                         resolution,
                         is_render_colours,
                         is_render_annotations,
                         is_render_depth):
    sensor_camera = Camera(name=name,
                           bng=bng,
                           vehicle=vehicle,
                           pos=pos,
                           resolution=resolution,
                           is_render_colours=is_render_colours,
                           is_render_annotations=is_render_annotations,
                           is_render_depth=is_render_depth)
    return sensor_camera

def save_camera_data(camera, output_dir):
    # Poll the camera sensor
    sensor_data = camera.poll()
    logging_mgr.log_action(f'Camera "{camera}" data polled.')

    # Split the sensor data
    color_image = sensor_data['colour']
    depth_image = sensor_data['depth']
    semantic_image = sensor_data['annotation']

    # Remove alpha channel from color image
    color_image = color_image.convert('RGB')

    # Save the images to the output directory
    color_image.save(os.path.join(output_dir, 'color.png'))
    depth_image.save(os.path.join(output_dir, 'depth.png'))
    semantic_image.save(os.path.join(output_dir, 'semantic.png'))
    logging_mgr.log_action(f'Camera "{camera}" data saved in "{output_dir}".')
