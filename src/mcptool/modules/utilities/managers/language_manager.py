import os
import sys

from typing import Union
from loguru import logger
from mccolors import mcwrite

from .json_manager import JsonManager
from .settings_manager import SettingsManager
from ..path.mcptool_path import MCPToolPath
from ..termux.termux_utilities import TermuxUtilities


class LanguageManager:
    def __init__(self):
        self.language = SettingsManager().get('language')

    @logger.catch
    def get(self, key: Union[list, str]) -> Union[dict, list, str, int, float, None]:
        """
        Method to get the language value

        Args:
            key (Union[list, str]): The key to get the value from

        Returns:
            Union[dict, list, str, int, float, None]: The value of the key
        """

        # Get the language file
        language_file: str = self.get_language()

        # Check if the language file exists
        # If it does not exist, log an error and close the program
        if not os.path.exists(language_file):
            logger.critical(f'Language file {language_file} does not exist')
            mcwrite(f'&8&l[&c&lCRITICAL ERROR&8&l] &c&lLanguage file does not exist &8&l(&f&lCheck the logs for more information (&b&l{MCPToolPath().get()}&f&l)&8&l)')
            sys.exit(1)

        value: Union[dict, list, str, int, float, None] = JsonManager(language_file).get(key)

        if value is None or value == 'None':
            logger.error(f'Key {key} does not exist in the language file')

        return value

    @logger.catch
    def set_language(self, language: str):  #! Actually, this method is not used in the code
        """
        Method to set the language

        Args:
            language (str): _description_
        """
        self.language: str = language

    @logger.catch
    def get_language(self) -> str:
        """
        Method to get the language file path

        Returns:
            str: The language file path
        """

        return os.path.join(MCPToolPath().get(), 'languages', f'{self.language}.json')
