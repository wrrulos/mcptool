import os

from loguru import logger

from ..path.mcptool_path import MCPToolPath
from .json_manager import JsonManager


class SettingsManager:
    def __init__(self):
        self.settings = JsonManager(os.path.join(MCPToolPath().get(), 'settings.json'))

    @logger.catch
    def get(self, key: str):
        """
        Method to get the value of a key in the settings file

        Args:
            key (str): The key to get the value from

        Returns:
            The value of the key
        """

        return self.settings.get(key)
    
    @logger.catch
    def set(self, key: str, value):
        """
        Method to set the value of a key in the settings file

        Args:
            key (str): The key to set the value
            value: The value to set
        """

        data = self.settings.read()
        data[key] = value
        self.settings.write(data)
