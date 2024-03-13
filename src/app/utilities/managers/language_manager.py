import os

from typing import Union

from src.app.logger import Logger
from . import json_manager


class LanguageManager:
    def __init__(self):
        self.language = "en"

    def get(self, key: Union[list, str]) -> str:
        """
        Method to get the text in the current language
        """

        # Get the language file
        language_file = self.get_language()

        # Check if the language file exists
        # If it does not exist, log an error and return 'None'
        if not os.path.exists(language_file):
            Logger().error(f'Language file {language_file} does not exist')
            return 'None'

        return json_manager.JsonManager(language_file).get(key)

    def set_language(self, language):
        self.language = language

    def get_language(self) -> str:
        """
        Method to get the language file path

        Returns:
            str: The language file path
        """

        return f'./languages/{self.language}.json'
