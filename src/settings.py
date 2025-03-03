import os
import utils

# Variables
# - Here are defined the setting variables used by the application
beamng_host: str = 'localhost'
beamng_port: int = 25252

# Routes
# - Here are defined the default routes used by the application
beamng_home_path: str = os.getenv('BNG_HOME')
weather_presets_path: str = os.path.join(beamng_home_path, 'gameengine.zip/art/weather/defaults.json')
output_root_path: str = utils.return_documents_path()