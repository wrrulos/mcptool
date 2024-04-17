from loguru import logger
from mccolors import mcwrite

from ..utilities.minecraft.player.get_player_uuid import PlayerUUID
from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'kick'
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]

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
        
        return True

    @logger.catch
    def execute(self, arguments: list) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        pass