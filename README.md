# BeamNG-Data-Capture
This project uses the BeamNG.tech Python API to capture and extract data from a BeamNG instance. It is intended to be used for generating datasets for artificial vision models in the field of autonomous driving.

The program can extract color image, depth and semantic annotation data from camera sensors, and metadata from the perspective vehicle, its sensors and the BeamNG instance running the simulation.

The settings of the capture session are defined by a scenario, which can be configured by the user as desired to use the desired perspective vehicle, sensors, map, starting location, etc.

_Note_: A BeamNG.tech licence is required for this capture program to work. Regular BeamNG.drive instances are not compatible.

## How to use
### Before launching
Make sure to have both Python and BeamNGpy installed (all project dependencies listed on `requirements.txt` file). This project has been tested to work with Python 3.10, earlier versions are not guaranteed to work.

It's recommended to use the most recent versions for both BeamNG.tech and BeamNGpy. At the time of development, these were version 0.34 and version 1.31, respectively.

It's required to set up the `BNG_HOME` environment variable with the BeamNG.tech folder path (for example, `C:\Users\[your_user]\Documents\BeamNG.tech`). Alternatively, set this path as the value for the `beamng_home_path` variable in the `settings.py` file.

### Launching
To execute the program and begin a capture session, open a console in the `src` folder and execute the following command:

```
python main.py
```

This will launch a BeamNG.tech instance and start a capture session with the default parameters defined in the `settings.py` file.

## Source files description
### Configuration files
Used to define the classes and their corresponding dictionaries for the different configurations used by the program. The data in these configurations can be customized by the user.

**camera_sensor_config.py**
: Defines the configuration used for the camera sensors.

**session_config.py**
: Defines the configuration used for the capture sessions.

**vehicle_config.py**
: Defines the configuration used for the vehicles.

### Manager files
Used to define functionatilies involving calls to the BeamNG.tech Python API.

**data_capture_mgr.py**
: Used to handle the data capturing from the simulation and metadata handling.

**logging_mgr.py**
: Used to manage calls to the BeamNG.tech logging module.

**scenario_mgr.py**
: Used to manage calls related to BeamNG scenarios and the currently loaded environment.

**simulation_mgr.py**
: Used to manage calls directed to the BeamNG simulator instance.

**vehicle_mgr.py**
: Used to manage calls regarding vehicles.

### General

**main.py**
: Defines the data capture initialization, capture loop and finish.

**settings.py**
: Defines the variables and configurations used by the program.

**utils.py**
: Defines generic or utility functions.