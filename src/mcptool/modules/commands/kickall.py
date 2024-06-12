import time

from loguru import logger
from typing import Union
from mccolors import mcwrite

from ..utilities.minecraft.server.get_server import MCServerData, JavaServerData, BedrockServerData
from ..utilities.minecraft.bot.server_response import BotServerResponse
from ..utilities.minecraft.bot.utilities import BotUtilities
from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'kickall'
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

        if not ValidateArgument.is_ip_and_port(arguments[0]):
            mcwrite(LM.get('errors.invalidIpAndPort'))
            return False

        if not ValidateArgument.is_yes_no(arguments[2]):
            mcwrite(LM.get('errors.invalidYesNo'))
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

        ip: str = arguments[0].split(':')[0]
        port: str = arguments[0].split(':')[1]
        version: str = arguments[1]
        loop: bool = arguments[2].lower() == 'y'

        # Get the server data to get the player list
        mcwrite(LM.get(f'commands.{self.name}.gettingPlayers').replace('%ip%', arguments[0]))
        server_data: Union[JavaServerData, BedrockServerData, None] = MCServerData(target=arguments[0], bot=False).get()

        if server_data is None:
            mcwrite(LM.get('errors.serverOffline'))
            return

        if server_data.platform != 'Java':
            mcwrite(LM.get('errors.notJavaServer'))
            return

        # Check if there are no players
        if len(server_data.player_list) == 0:
            mcwrite(LM.get(f'commands.{self.name}.noPlayers').replace('%ip%', arguments[0]))
            return

        # Loop through the players and kick them
        for player in server_data.player_list:
            username: str = player['name']

            # Kick the player
            bot_response: str = BotServerResponse(ip_address=ip, port=int(port), version=version, username=username).get_response()

            # Check if the player was kicked
            if bot_response == 'Connected':
                mcwrite(LM.get('commands.kick.playerKicked')
                    .replace('%username%', username)
                )

            else:
                # Get the bot color response
                bot_response: str = BotUtilities.get_bot_color_response(bot_response)

                mcwrite(LM.get('commands.kick.playerNotKicked')
                    .replace('%username%', username)
                    .replace('%reason%', bot_response)
                )

            time.sleep(BotUtilities.get_bot_reconnect_time())

        mcwrite(LM.get(f'commands.{self.name}.allPlayersKicked'))

        # Check if the command should loop
        if loop:
            self.execute(arguments)
