import os
from logging import Logger, INFO
import json
from typing import Dict, List
import urllib.request
import re

import toml
import yaml
from deepmerge import always_merger

class Config:
    """
    This class emulates the Spring Boot functionality.
    Currently only YML files are supported.
    """

    allowed_extensions = ['yml', 'toml']

    def __init__(self, profiles: List[str] = ['default'], locations: List[str] = ['./', './config/'], logger: Logger = None, log_level=INFO) -> None:
        """
        Parameters
        ----------
        profiles : List[str] 
            List of all required profiles. Default value is ['default']
        locations : List[str] 
            List of paths where this class will scan for configuration files
        logger: Logger
            Inject optional logger
        log_level: str
            Log level for default logger if no logger provided
        """
        # init logger if not provided
        if logger == None:
            logger = Logger('ecmind_spring_config', log_level)
        
        self.logger = logger

        # init empty configuration
        self._config: Dict[str, any] = {}

        # load environment into config
        self.logger.debug('Parse environment')
        for key in os.environ.keys():
            self.put(self.to_camel_case(key), os.environ.get(key))

        # check if key spring.profiles.active is set and load this profiles. 
        # The environment parameter will overwrite the function parameter
        if self.get('spring.profiles.active') == None:
            self.put('spring.profiles.active', profiles)

        self.logger.debug(f'Active profiles are {self.get_profiles()}')

        # check if key spring.config.location is set and load this locations. 
        # The environment parameter will overwrite the function parameter       
        if self.get('spring.config.location') == None:
            self.put('spring.config.location', locations)

        locations = self.get_locations()
        self.logger.debug(f'Config locations are {locations}')

        # check each location
        for location in locations:
            # load config directly if location is a file path
            if os.path.isfile(location):
                self.logger.debug(f'Parse config {locations}')
                self._parse_config_file(location)
            # check for expected config files if location is a path
            elif os.path.isdir(location):
                for extension in Config.allowed_extensions:
                    filepath = location + f"/application.{extension}"
                    if os.path.isfile(filepath):
                        self.logger.debug(f'Parse config {filepath}')
                        self._parse_config_file(filepath)
                    #check for each profile name if a config file exists
                    for profile in self.get_profiles():
                        filepath = location + f"/application-{profile}.{extension}"
                        if os.path.isfile(filepath):
                            self.logger.debug(f'Parse config {filepath}')
                            self._parse_config_file(filepath)
        
        # Overwrite file config with environment
        self.logger.debug('Reparse environment')
        for key in os.environ.keys():
            self.put(self.to_camel_case(key), os.environ.get(key))

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
        key = key.lower()

        item = self._config
        for key_part in key.split("."):
            found = False
            for item_key in item.keys():
                if item_key.lower() == key_part:
                    item = item[item_key]
                    found = True
                    break
            if not found: 
                return default

        item = self.replace_variables(item)


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

    def put(self, key: str, value: any, data: Dict[str, any] = None):
        """
        Method to set a config value

        Parameters
        ----------
        key : str 
            config key like spring or also deep keys like spring.profiles.active
        value : str 
            new value under the defined key
        data: Dict 
            Dict of the config. Keep this empty
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

    def get_profiles(self) -> List[str]:
        """
        returns the defined profiles as List of strings
        """

        profiles = self.get('spring.profiles.active')
        return profiles if isinstance(profiles, List) else [p.strip() for p in profiles.split(',')]

    def get_locations(self) -> List[str]:
        """
        returns the defined locations as List of strings
        """

        locations = self.get('spring.config.location')
        return locations if isinstance(locations, List) else [p.strip() for p in locations.split(',')]

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
        label = self.get('spring.cloud.config.label')
        app_name = self['spring.application.name']
        profiles = ",".join(self.get_profiles())

        if uri == None:
            return

        if app_name == None:
            raise ValueError('If spring.cloud.config.uri is set spring.application.name is required')

        if label:
            address = f'{uri}/{label}/{app_name}-{profiles}.json'
        else:
            address = f'{uri}/{app_name}-{profiles}.json'

        self.logger.info(
            f"Try to load configuration from spring cloud config server at {address}")

        try:
            with urllib.request.urlopen(address) as response:
                config = json.loads(response.read())
                # Keys to lower case
                #config = self._make_lowercase(config)

                self._config = always_merger.merge(self._config, config)

        except urllib.error.URLError as e:
            self.logger.error(e.reason)
            raise e

    def replace_variables(self, obj):
        if isinstance(obj, dict):
            ret = {}
            for k,v in obj.items():
                ret[k] = self.replace_variables(v)
            return ret
        elif isinstance(obj, str):
            for m in re.finditer('\$\{(?P<key1>[^\}]+):(?P<fallback>[^}]+)\}|\$\{(?P<key2>[^\}]+)\}', obj):
                match = m.group(0)
                key = m.group('key1') if m.group('key1') else m.group('key2')
                fallback = m.group('fallback')
                
                replacement = self.get(key)
                if replacement == None:
                    if fallback:
                        replacement = fallback
                    else:
                        replacement = ''
                obj = obj.replace(match, replacement, 1)


            return obj
        elif hasattr(obj,'__iter__'):
            ret = []
            for item in obj:
                ret.append(self.replace_variables(item))
            return ret
        else:
            return obj

    def to_camel_case(self, snake_str: str):
        components = snake_str.lower().split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
                    