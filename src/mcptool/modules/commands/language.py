from loguru import logger
from typing import Union
from mccolors import mcwrite
from easyjsonpy import get_config_value, set_language, set_config_value

from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'language'
        self.arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]
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
            mcwrite(LM.get('errors.invalidLanguage'))
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

        if get_config_value('language') == self.language:
            mcwrite(LM.get(f'commands.{self.name}.sameLanguage').replace('%language%', self.language))
            return

        set_language(self.language)
        set_config_value('language', self.language)
        mcwrite(LM.get(f'commands.{self.name}.languageChanged').replace('%language%', self.language))
