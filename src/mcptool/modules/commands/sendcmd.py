import subprocess
import os

from loguru import logger
from typing import Union
from mccolors import mcwrite

from ..utilities.minecraft.player.get_player_uuid import PlayerUUID
from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.commands.validate import ValidateArgument
from ..utilities.minecraft.server.get_server import MCServerData, JavaServerData, BedrockServerData
from ..utilities.path.mcptool_path import MCPToolPath
from ..utilities.constants import OS_NAME, SPACES

class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'sendcmd'
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]
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
            mcwrite(LM().get(['errors', 'invalidIpAndPort']))
            return False
        
        if not os.path.exists(arguments[3]):
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
        
        ip_address: str = arguments[0].split(':')[0]
        port: str = arguments[0].split(':')[1]
        version: str = arguments[1]
        username: str = arguments[2]
        commands_file: str = arguments[3]
                
        server_data: Union[JavaServerData, BedrockServerData, None] = MCServerData(target=arguments[0], bot=False).get()

        if server_data is None:
            mcwrite(LM().get(['errors', 'serverOffline']))
            return
        
        if server_data.platform != 'Java':
            mcwrite(LM().get(['errors', 'notJavaServer']))
            return
        
        mcwrite(LM().get(['commands', self.name, 'gettingCommands']).replace('%file%', commands_file))

        # Check if the commands file is empty
        with open(commands_file, 'r') as file:
            commands = file.read().splitlines()

        if len(commands) == 0:
            mcwrite(LM().get(['errors', 'commandsFileEmpty']))
            return
        
        path: str = MCPToolPath().get()
        command: str = f'cd {path} && node scripts/sendcmd.mjs {ip_address} {port} {username} {version} {commands_file} {SPACES}'
        
        if OS_NAME == 'windows':
            command = f'C: && {command}'
        
        # Start sending the commands to the server
        mcwrite(LM().get(['commands', self.name, 'sendingCommands'])
            .replace('%ip%', f'{ip_address}:{port}')
            .replace('%username%', username)
            .replace('%commandsFile%', commands_file)
            .replace('%commands%', str(len(commands)))
        )
        subprocess.run(command, shell=True)
