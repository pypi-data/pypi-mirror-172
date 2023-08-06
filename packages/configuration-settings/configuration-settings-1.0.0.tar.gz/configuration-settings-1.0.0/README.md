# configuration_settings module

General purpose config file parser.


### Installation

Install with pip:

    pip install configuration-settings


### Usage

Load a set of config files:

    from configuration_settings import Config

    config = Config.load(__file__)

You may optionally pass a path to a specific config file (generally passed as a command line argument),
and a dict containing default values.

    def load(cls, script_path: str, config_path: str = None, default: Mapping[str, Any] = None) -> Config:

Config files may be JSON or YAML, and can contain arbitrary structure.
Dicts in config files are converted to Config objects.
Names (keys) are case-insensitive.

Config files are loaded from the following locations:

* If no config path is provided:

  * All parent directories from the location the script is located
  * The directory the script is located
  * /etc/{script_name}
  * The current directory

* If a config path is provided 

  * All parent directories from the location the script is located
  * The directory the script is located
  * The provided config path

For each location,
if the location is a file, load that file, 
then search the file's directory for directories named: 
'conf.d', 'config.d', '{script_name}.d', '{file_name}.d',
load all files in those directories in alphabetical order.
If the location is a directory, search for files named: 
'config', 'config.local', '{script_name}', '{script_name}.local',
then search for subdirectories named:
'conf.d', 'config.d', '{script_name}.d', '{file_name}.d'.

Files loaded later override values found in earlier files.
Dict values are merged so only provided keys are replaced.

Config files may have the following extensions: '.json', '.yml', '.yaml'.

Common usage would be to have a config file with default values installed in the same location as the main script,
and then the user would override settings in /etc/{script_name}/config.yaml and /etc/{script_name}/config.d/*.yaml.

Config objects are dict-like and also allow accessing values as properties.


In addition, there are methods to get values as a specific type:

    def get_int(self, name: str, default: int = None) -> (int | None):
        """
        Get an item as an int.

        Returns default if missing or not an int.
        """

    def get_float(self, name: str, default: float = None) -> (float | None):
        """
        Get an item as a float.

        Returns default if missing or not a float.
        """

    def get_bool(self, name: str, default: bool = None) -> (bool | None):
        """
        Get an item as a bool.

        Returns default if missing or not a bool.
        """

    def get_path(self, name: str, default: str = None) -> (str | None):
        """
        Get an item as an absolute path.

        Relative paths are resolved to the config file the item was loaded from.
        Returns default if missing.
        """
    def get_duration(self, name: str, default: timedelta = None) -> (timedelta | None):
        """
        Get an item as a timedelta.

        Accepts int values (seconds),
        or string values with s|m|h|d|w suffix for seconds, minutes, hours, days, or weeks.
        """


You can set a default value for any item via:

    def set_default(self, name: str, value: Any) -> None:


You can retrieve the full set of patsh to config files via the `config_file_paths` property,
or get the file a specific value was loaded from via:

    def get_config_file_path(self, name: str) -> (str | None):