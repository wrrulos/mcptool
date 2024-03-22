import logging

from typing import Union
from mccolors import mcwrite

from src.mcptool.utilities.minecraft.server.get_server import BedrockServerData, JavaServerData, MCServerData
from src.mcptool.utilities.minecraft.server.show_server import ShowMinecraftServer
from src.mcptool.utilities.managers.language_manager import LanguageManager as LM
from src.mcptool.utilities.commands.validate import ValidateArgument


class Command:
    def __init__(self):
        self.name: str = 'server'
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
        
        server: str = arguments[0]

        if not validate.is_domain(server) and not validate.is_ip_and_port(server):
            mcwrite(LM().get(['errors', 'invalidServerFormat']))
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
        
        # Get the server data
        mcwrite(LM().get(['commands', 'server', 'gettingServerData']))
        server_data: Union[JavaServerData, BedrockServerData, None] = MCServerData(arguments[0]).get()

        # Check if the server data is None
        if server_data is None:
            mcwrite(LM().get(['commands', 'server', 'serverOffline']))
            return

        # Show the server data
        ShowMinecraftServer().show(server_data=server_data)
