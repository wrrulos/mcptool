import time

from loguru import logger
from mccolors import mcwrite

from ..utilities.minecraft.bot.server_response import BotServerResponse
from ..utilities.minecraft.bot.utilities import BotUtilities
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
        
        if not ValidateArgument.is_ip_and_port(arguments[0]):
            mcwrite(LM().get(['errors', 'invalidIpAndPort']))
            return False
        
        if not ValidateArgument.is_yes_no(arguments[3]):
            mcwrite(LM().get(['errors', 'invalidYesNo']))
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
        username: str = arguments[2]
        loop: str = arguments[3]
        
        mcwrite(LM().get(['commands', 'kick', 'kickingPlayer'])
            .replace('%ip%', arguments[0])
            .replace('%version%', arguments[1])
            .replace('%username%', arguments[2])
        )

        # Kick the player
        bot_response: str = BotServerResponse(ip_address=ip, port=int(port), version=version, username=username).get_response()

        # Check if the player was kicked
        if bot_response == 'Connected':
            mcwrite(LM().get(['commands', 'kick', 'playerKicked'])
                .replace('%username%', arguments[2])
            )

        else:
            # Get the bot color response
            bot_response: str = BotUtilities.get_bot_color_response(bot_response)

            mcwrite(LM().get(['commands', 'kick', 'playerNotKicked'])
                .replace('%username%', arguments[2])
                .replace('%reason%', bot_response)
            )

        if loop:
            time.sleep(BotUtilities.get_bot_reconnect_time())
            self.execute(arguments)
