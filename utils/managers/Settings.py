#!/usr/bin/python3

import json


class SettingsManager:
    def __init__(self) -> None:
        pass

    def open(self, file):
        """ Open the configuration file and return the data """
        
        with open(f'settings/{file}.json', 'r') as f:
            settings = json.loads(f.read())
            return settings

    def read(self, file):
        """ Read the configuration and return it """

        mcptool_config = self.open(file)
        return mcptool_config

    def write(self, file, option, value):
        """ Overwrite the configuration """

        settings = self.read(file)
        settings[option] = value

        with open(f'settings/{file}.json', 'w+') as f:
            json.dump(settings, f, indent=4)
