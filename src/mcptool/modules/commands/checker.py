import re
import os

from loguru import logger
from typing import Union
from mccolors import mcwrite

from ..utilities.minecraft.server.get_server import MCServerData, JavaServerData, BedrockServerData
from ..utilities.minecraft.server.show_server import ShowMinecraftServer
from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'checker'
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]
        self.servers_found: int = 0

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

        if not os.path.exists(arguments[0]):
            mcwrite(LM().get(['errors', 'invalidFile']))
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

        file: str = arguments[0]

        # Read the file
        with open(file, 'r') as f:
            lines: list = f.readlines()

        mcwrite(LM().get(['commands', self.name, 'checking'])
            .replace('%file%', file)
        )

        # Check the lines
        for line in lines:
            ips_and_ports: list = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)

            if len(ips_and_ports) == 0:
                continue

            for ip_and_port in ips_and_ports:
                server_data: Union[JavaServerData, BedrockServerData] = MCServerData(target=ip_and_port).get()

                if server_data is not None:
                    ShowMinecraftServer.show(server_data=server_data)
                    self.servers_found += 1

        if self.servers_found == 0:
            mcwrite(LM().get(['commands', self.name, 'noServersFound'])
                .replace('%file%', file)
            )
            return

        mcwrite(LM().get(['commands', self.name, 'serversFound'])
            .replace('%servers%', str(self.servers_found))
            .replace('%file%', file)
        )
