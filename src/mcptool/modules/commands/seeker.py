from typing import Union
from mccolors import mcwrite
from loguru import logger
from easyjsonpy import get_config_value, set_config_value

from ..utilities.seeker.utilities import SeekerUtilities
from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.commands.validate import ValidateArgument
from ..utilities.minecraft.server import JavaServerData, BedrockServerData
from ..utilities.minecraft.server.show_server import ShowMinecraftServer
from ..utilities.minecraft.server.get_server import ServerData


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'seeker'
        self.token: Union[str, None] = get_config_value('seekerToken')
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

        if not ValidateArgument.is_seeker_subcommand(arguments[0]):
            print('invalid sub command')
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

        if arguments[0] == 'token':
            self._get_token()

        if arguments[0] == 'servers':
            self._get_servers()

    @logger.catch
    def _get_token(self) -> None:
        """
        Method to get the token from the user
        and save it in the settings
        """

        TOKEN: str = SeekerUtilities.get_token()

        if TOKEN == '':
            return

        # Save the token in the settings
        self.token = TOKEN
        set_config_value('seekerToken', TOKEN)

    @logger.catch
    def _get_servers(self) -> None:
        """
        Method to get the servers from the seeker API
        """

        if self.token is None:
            mcwrite(LM.get(f'commands.{self.name}.token.invalidToken'))
            return

        # Get the servers
        servers = SeekerUtilities.get_servers(self.token)

        if len(servers) == 0:
            mcwrite(LM.get(f'commands.{self.name}.servers.noServers'))
            return

        mcwrite(LM.get(f'commands.{self.name}.servers.gettingServers'))

        # Print the servers
        for server in servers:
            if 'server' not in server:
                continue

            server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(target=server['server']).get_data()

            if server_data is None:
                continue

            ShowMinecraftServer.show(server_data=server_data)
