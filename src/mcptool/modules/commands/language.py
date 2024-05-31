from loguru import logger
from typing import Union
from mccolors import mcwrite

from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.managers.settings_manager import SettingsManager as SM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'language'
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]
        self.language: Union[str, None] = None
        self.servers_found: int = 0

    @logger.catch
    def validate_arguments(self, arguments: list) -> bool:
        """
        Method to validate the arguments

        Args:
            arguments (list): The arguments to validate

        Returns:
            bool: True if the arguments are valid, False otherwise
        """

        if not ValidateArgument.validate_arguments_length(command_name=self.name, command_arguments=self.arguments, user_arguments=arguments):
            return False

        self.language = arguments[0]

        if not ValidateArgument.is_valid_language(self.language):
            mcwrite(LM().get(['errors', 'invalidLanguage']))
            return False

        return True

    @logger.catch
    def execute(self, arguments: list) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        # Validate the arguments
        if not self.validate_arguments(arguments):
            return

        if SM().get('language') == self.language:
            mcwrite(LM().get(['commands', self.name, 'sameLanguage']).replace('%language%', self.language))
            return

        LM().set_language(self.language)
        mcwrite(LM().get(['commands', self.name, 'languageChanged']).replace('%language%', self.language))
