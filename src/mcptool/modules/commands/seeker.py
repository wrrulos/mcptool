from typing import Union
from mccolors import mcwrite
from loguru import logger

from ..utilities.seeker.utilities import SeekerUtilities
from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.managers.settings_manager import SettingsManager as SM
from ..utilities.commands.validate import ValidateArgument
from ..utilities.minecraft.server.get_server import MCServerData, JavaServerData, BedrockServerData
from ..utilities.minecraft.server.show_server import ShowMinecraftServer


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'seeker'
        self.token: Union[str, None] = SM().get('seekerToken')
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

        validate = ValidateArgument(command_name=self.name, command_arguments=self.arguments, user_arguments=arguments)

        if not validate.validate_arguments_length():
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
        SM().set(key='seekerToken', value=self.token)

    @logger.catch
    def _get_servers(self) -> None:
        """
        Method to get the servers from the seeker API
        """

        if self.token is None:
            mcwrite(LM().get(['commands', self.name, 'token', 'invalidToken']))
            return

        # Get the servers
        servers = SeekerUtilities.get_servers(self.token)

        if len(servers) == 0:
            mcwrite(LM().get(['commands', self.name, 'servers', 'noServers']))
            return

        # Print the servers
        for server in servers:
            if 'server' not in server:
                continue

            server_data: Union[JavaServerData, BedrockServerData, None] = MCServerData(target=server['server']).get()

            if server_data is None:
                continue

            ShowMinecraftServer().show(server_data=server_data)
