import json
import os

from typing import Union
from loguru import logger

from ..constants import PREFIX, SPACES


class JsonManager:
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path

    def read(self) -> dict:
        """
        Method to read the json file

        Returns:
            dict: The data in the json file
        """

        # Check if the json file exists
        # If it does not exist, log an error and return an empty dictionary
        if not os.path.exists(self.json_file_path):
            logger.error(f'Json file {self.json_file_path} does not exist')
            return {}

        with open(self.json_file_path, 'r', encoding='utf8') as file:
            return json.load(file)

    def write(self, data: dict) -> None:
        """
        Method to write data to the json file

        Args:
            data (dict): The data to write to the json file
        """

        with open(self.json_file_path, 'w', encoding='utf8') as file:
            json.dump(data, file, indent=4)

    def get(self, key: Union[str, list]) -> Union[dict, list, str, int, float, None]:
        """
        Method to get the value of a key in the json file

        Args:
            key (Union[str, list]): The key to get the value from

        Returns:
            Union[dict, list, str, int, float, None]: The value of the key
        """

        # Read the json file
        data = self.read()

        try:
            # Check if the key is a list
            if isinstance(key, list):
                for k in key:
                    data = data.get(k, 'None')

                if '%spaces%' in data:
                    data = data.replace('%spaces%', ' ' * SPACES)

                if '%prefix%' in data:
                    data = data.replace('%prefix%', PREFIX)

                return data

            if '%spaces%' in data:
                data = data.replace('%spaces%', ' ' * SPACES)

            if '%prefix%' in data:
                data = data.replace('%prefix%', PREFIX)

            return data.get(key, 'None')
            
        except AttributeError:
            return None
