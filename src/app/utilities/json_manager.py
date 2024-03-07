import json
import os

from typing import Union


class JsonManager:
    def __init__(self, json_file):
        self.json_file = json_file

    def read(self) -> dict:
        if not os.path.exists(self.json_file):
            return {}
        
        with open(self.json_file, 'r', encoding='utf8') as file:
            return json.load(file)

    def write(self, data):
        with open(self.json_file, 'w', encoding='utf8') as file:
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

        # Check if the key is a list
        if isinstance(key, list):
            for k in key:
                data = data.get(k, 'None')
                
            return data
        
        return data.get(key, 'None')