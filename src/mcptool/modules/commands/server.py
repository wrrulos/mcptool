from typing import Union
from mccolors import mcwrite
from loguru import logger

from ..utilities.minecraft.server import BedrockServerData, JavaServerData
from ..utilities.minecraft.server.get_server import ServerData
from ..utilities.minecraft.server.show_server import ShowMinecraftServer
from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'server'
        self.arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]

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

        if not ValidateArgument.is_domain(domain=server) and not ValidateArgument.is_ip_and_port(ip=server) and not ValidateArgument.is_domain_and_port(domain=server):
            mcwrite(LM.get('errors.invalidServerFormat'))
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
        mcwrite(LM.get(f'commands.{self.name}.gettingServerData'))
        server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(arguments[0]).get_data()

        # Check if the server data is None
        if server_data is None:
            mcwrite(LM.get('errors.serverOffline'))
            return

        # Show the server data
        ShowMinecraftServer.show(server_data=server_data)
