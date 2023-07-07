import json

from utils.managers.config_manager import config_manager


class LanguageManager:
    def __init__(self):
        self.file = f'config/lang/{config_manager.config["lang"]}.json'
        self.language = {}
        self.load_language()

    def load_language(self):
        """
        Read the configuration file and get the language and then return it.

        Args:
            self: Instance of the class containing the 'self.file' attribute.

        Returns:
            dict: Dictionary containing the configuration data.
        """

        with open(self.file, 'r', encoding='utf8') as f:
            self.language = json.load(f)


language_manager = LanguageManager()
