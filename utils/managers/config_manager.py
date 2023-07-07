import json


class ConfigManager:
    def __init__(self, file):
        self.file = file
        self.config = {}
        self.load_config()

    def load_config(self):
        """
        Read the configuration file and get the configuration and then return it.

        Args:
            self: Instance of the class containing the 'self.file' attribute.

        Returns:
            dict: Dictionary containing the configuration data.
        """

        with open(self.file, 'r', encoding='utf8') as f:
            self.config = json.load(f)

    def update_settings(self, new_settings):
        """
        Update config
        """

        self.config.update(new_settings)

        with open(self.file, 'w', encoding='utf8') as f:
            json.dump(self.config, f, indent=4)


config_manager = ConfigManager('config/config.json')
