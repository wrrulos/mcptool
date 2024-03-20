from mccolors import mcwrite

from src.mcptool.utilities.ip.get_ip_info import IPInfo
from src.mcptool.utilities.managers.language_manager import LanguageManager as LM
from src.mcptool.utilities.commands.validate import ValidateArgument


class Command:
    def __init__(self):
        self.name: str = 'ipinfo'
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]

    def validate_arguments(self, arguments: list) -> bool:
        """
        Method to validate the arguments

        Args:
            arguments (list): The arguments to validate

        Returns:
            bool: True if the arguments are valid, False otherwise
        """

        validate = ValidateArgument(command_name=self.name, command_arguments=self.arguments, user_arguments=arguments)

        if not validate.validate_arguments_length():
            return False
        
        if not ValidateArgument.is_ip_address(arguments[0]):
            mcwrite(LM().get(['errors', 'invalidIpFormat']))
            return False
        
        return True

    def execute(self, arguments: list) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        # Validate the arguments
        if not self.validate_arguments(arguments):
            return
        
        # Get the player data
        mcwrite(LM().get(['commands', 'ipinfo', 'gettingIpData']))
        
        # Get the IP address information
        ip_info = IPInfo(ip_address=arguments[0]).get_info()

        if ip_info is None:
            mcwrite(LM().get(['commands', 'ipinfo', 'error']))
            return
        
        mcwrite(ip_info.continent)
