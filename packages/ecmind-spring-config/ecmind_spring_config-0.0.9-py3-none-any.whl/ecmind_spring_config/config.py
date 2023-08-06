import os
import logging
import json
import urllib.request

import toml
import yaml
from deepmerge import always_merger

class Config:
    """
    This class emulates the Spring Boot functionality.
    Currently only YML files are supported.
    """

    allowed_extensions = ['yml', 'toml']

    def __init__(self, profiles: list[str] = ['default'], locations: list[str] = ['./', './config/']) -> None:
        """
        Parameters
        ----------
        profiles : list[str] 
            List of all required profiles. Default value is ['default']
        locations : list[str] 
            List of paths where this class will scan for configuration files
        """
        
        # init empty configuration
        self._config: dict[str, any] = {}

        # load environment into config
        logging.debug('Parse environment')
        for key in os.environ.keys():
            self.put(key, os.environ.get(key))

        # check if key spring.profiles.active is set and load this profiles. 
        # The environment parameter will overwrite the function parameter
        if self.get('spring.profiles.active') == None:
            self.put('spring.profiles.active', profiles)

        logging.debug(f'Active profiles are {self.get_profiles()}')

        # check if key spring.config.location is set and load this locations. 
        # The environment parameter will overwrite the function parameter       
        if self.get('spring.config.location') == None:
            self.put('spring.config.location', locations)

        locations = self.get_locations()
        logging.debug(f'Config locations are {locations}')

        # check each location
        for location in locations:
            # load config directly if location is a file path
            if os.path.isfile(location):
                logging.debug(f'Parse config {locations}')
                self._parse_config_file(location)
            # check for expected config files if location is a path
            elif os.path.isdir(location):
                for extension in Config.allowed_extensions:
                    filepath = location + f"/application.{extension}"
                    if os.path.isfile(filepath):
                        logging.debug(f'Parse config {filepath}')
                        self._parse_config_file(filepath)
                    #check for each profile name if a config file exists
                    for profile in self.get_profiles():
                        filepath = location + f"/application-{profile}.{extension}"
                        if os.path.isfile(filepath):
                            logging.debug(f'Parse config {filepath}')
                            self._parse_config_file(filepath)
        
        # load from spring cloud config server if possible 
        self.load_cloud_config()

    def __getitem__(self, key: str):
        """
        Dict like interface implementation for config[key]. 
        
        Parameters
        ----------
        key : str 
            config key like spring or also deep keys like spring.profiles.active
        
        Returns the value or None if not found
        """
        return self.get(key, None)

    def get(self, key: str, default: any = None) -> any:
        """
        returns the value for the specified key if it exists. Otherwise the default value is returned.
        
        Parameters
        ----------
        key : str 
            config key like spring or also deep keys like spring.profiles.active
        default : any 
            Default value if key was not found. Default value is None if not set.
        
        Returns the value or default if not found
        """
        item = self._config
        try:
            for key_part in key.split("."):
                item = item[key_part]
        except KeyError:
            return default

        return item

    def __setitem__(self, key: str, value: any):
        """
        Dict like interface implementation for config[key] = value. 
        
        Parameters
        ----------
        key : str 
            config key like spring or also deep keys like spring.profiles.active
        value : str 
            new value under the defined key
        """
        self.put(key, value)

    def put(self, key: str, value: any, data: dict[str, any] = None):
        """
        Method to set a config value

        Parameters
        ----------
        key : str 
            config key like spring or also deep keys like spring.profiles.active
        value : str 
            new value under the defined key
        data: dict 
            dict of the config. Keep this empty
        """
        if data == None:
            data = self._config
        
        if "." in key:
            key, rest = key.split(".", 1)
            if key not in data:
                data[key] = {}

            self.put(rest, value, data[key])
        else:
            data[key] = value

    def get_profiles(self) -> list[str]:
        """
        returns the defined profiles as list of strings
        """

        profiles = self.get('spring.profiles.active')
        return profiles if isinstance(profiles, list) else [p.strip() for p in profiles.split(',')]

    def get_locations(self) -> list[str]:
        """
        returns the defined locations as list of strings
        """

        locations = self.get('spring.config.location')
        return locations if isinstance(locations, list) else [p.strip() for p in locations.split(',')]

    def _parse_config_file(self, filepath: str):
        """
        Parse configuration and add the result to the configuration
        Parameters
        ----------
        filepath : str 
            filepath to the configuration
        """
        if filepath.endswith('yml'):
            config = yaml.load(open(filepath), Loader=yaml.FullLoader)
            self._config = always_merger.merge(self._config, config)
        elif filepath.endswith('toml'):
            config = toml.load(filepath)
            self._config = always_merger.merge(self._config, config)

    def load_cloud_config(self):
        """
        Try to load configuration from the Spring Cloud Config Server.
        
        the following keys have to be set correctly:
        - spring.cloud.config.uri
        - spring.application.name
        """

        uri = self.get('spring.cloud.config.uri')
        app_name = self['spring.application.name']
        profiles = ",".join(self.get_profiles())

        if uri == None:
            return

        if app_name == None:
            raise ValueError('Key spring.application.name is required')

        logging.info(
            f"Try to load configuration from spring cloud config server at {self['spring.cloud.config.uri']}")

        address = f'{uri}/{app_name}-{profiles}.json'

        try:
            with urllib.request.urlopen(address) as response:
                config = json.loads(response.read())
                self._config = always_merger.merge(self._config, config)

        except urllib.error.URLError as e:
            logging.error(e.reason)
            raise e
