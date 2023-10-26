import os
import json


class JsonManager:
    @staticmethod
    def load_json(file_path):
        """
        Loads the content from the specified file.

        Args:
            file_path (str): Path to the configuration file.

        Returns:
            dict: Loaded configuration as a dictionary.
        """

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf8') as f:
                return json.loads(f.read())

        return JsonManager.DEFAULT_CONFIG

    @staticmethod
    def save_json(content, file_path):
        """
        Saves the content to the specified file.

        Args:
            content (dict): Configuration dictionary to be saved.
            file_path (str): Path to the configuration file.
        """

        with open(file_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(content, indent=4))

    @staticmethod
    def get(key, file_path='./config/config.json'):
        """
        Gets the value associated with the specified key from the configuration.

        Args:
            file_path (str): Path to the JSON configuration file.
            key (str or list): Key or list of keys to retrieve the value for.

        Returns:
            Any: Value associated with the key, or None if not found.
        """
        
        content = JsonManager.load_json(file_path)
        
        if isinstance(key, list):
            value = content
            for k in key:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return None  # Key doesn't exist in the dictionary structure
            return value
        
        else:
            return content.get(key)