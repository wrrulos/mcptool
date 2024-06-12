from loguru import logger
from mccolors import mcwrite, mcreplace
from typing import Union
from mcrcon import MCRcon, MCRconException

from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.commands.validate import ValidateArgument
from ..utilities.constants import SPACES


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'rcon'
        self.arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]
        self.passwords: list = []

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

        ip_address: str = arguments[0].split(':')[0]
        port: str = arguments[0].split(':')[1]
        rcon_password: str = arguments[1]
        mcr: Union[MCRcon, None] = None

        mcwrite(LM.get(f'commands.{self.name}.connecting')
            .replace('%ip%', f'{ip_address}:{port}')
        )

        try:
            with MCRcon(host=ip_address, password=rcon_password, port=int(port), timeout=30) as mcr:
                mcwrite(LM.get(f'commands.{self.name}.connected'))

                while True:
                    command: str = input(mcreplace(LM.get(f'commands.{self.name}.commandInput')))

                    if command == '.exit':
                        mcwrite(LM.get(f'commands.{self.name}.disconnected'))
                        mcr.disconnect()
                        break

                    response: str = mcr.command(command)
                    mcwrite(f'{SPACES}{response}')

        except TimeoutError:
            mcwrite(LM.get('errors.rconTimeout'))

        except ConnectionRefusedError:
            mcwrite(LM.get('errors.rconConnectionRefused'))

        except MCRconException:
            mcwrite(LM.get('errors.rconInvalidPassword'))

        except KeyboardInterrupt:
            if mcr:
                mcr.disconnect()

            mcwrite(LM.get(f'commands.{self.name}.disconnected'))

        except Exception as e:
            mcwrite(LM.get('errors.rconUnknownError'))
            logger.error(f'Error in rcon command: {e}')
