import time

from loguru import logger
from mccolors import mcwrite
from typing import Union

from ..utilities.minecraft.player.get_player_uuid import PlayerUUID
from ..utilities.minecraft.server import JavaServerData, BedrockServerData
from ..utilities.minecraft.server.get_server import ServerData
from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'listening'
        self.arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]
        self.attempts: int = 0
        self.players: list = []

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

        if not ValidateArgument.is_ip_and_port(arguments[0]):
            mcwrite(LM.get('errors.invalidIpAndPort'))
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

        mcwrite(LM.get(f'commands.{self.name}.connecting').replace('%ip%', arguments[0]))

        # Get the server data
        server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(target=arguments[0], bot=False).get_data()

        if server_data is None:
            mcwrite(LM.get('errors.serverOffline'))
            return

        if server_data.platform != 'Java':
            mcwrite(LM.get('errors.notJavaServer'))
            return

        mcwrite(LM.get(f'commands.{self.name}.waitingForConnections').replace('%ip%', arguments[0]))

        while True:
            server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(target=arguments[0], bot=False).get_data()

            # Check if the server is offline
            if server_data is None:
                self.attempts += 1
                time.sleep(30)
                continue

            # Check if the server has players
            if len(server_data.player_list) == 0:
                continue

            for player in server_data.player_list:
                # If there are no players, print the message
                if len(self.players) == 0:
                    mcwrite(LM.get(f'commands.{self.name}.playersFound'))

                if player not in self.players:
                    self.players.append(player)

                    if player['id'] is None:
                        continue

                    uuid_color: str = PlayerUUID(username=player['name']).get_uuid_color(player['id'])

                    mcwrite(LM.get(f'commands.{self.name}.playerFoundFormat')
                            .replace('%username%', player['name'])
                            .replace('%uuid%', f"{uuid_color}{player['id']}")
                    )

            time.sleep(1)
