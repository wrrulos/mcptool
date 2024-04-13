from typing import Union
from mccolors import mcwrite
from loguru import logger

from ..utilities.minecraft.server.get_server import BedrockServerData, JavaServerData, MCServerData
from ..utilities.minecraft.server.show_server import ShowMinecraftServer
from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'server'
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
        
        server: str = arguments[0]

        if not ValidateArgument.is_domain(domain=server) and not ValidateArgument.is_ip_and_port(ip=server):
            mcwrite(LM().get(['errors', 'invalidServerFormat']))
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
        
        # Get the server data
        mcwrite(LM().get(['commands', 'server', 'gettingServerData']))
        server_data: Union[JavaServerData, BedrockServerData, None] = MCServerData(arguments[0]).get()

        # Check if the server data is None
        if server_data is None:
            mcwrite(LM().get(['commands', 'server', 'serverOffline']))
            return

        print(server_data, type(server_data))
        # Show the server data
        ShowMinecraftServer.show(server_data=server_data)
