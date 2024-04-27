import subprocess
import os

from loguru import logger

# Import the MCPToolPath class
from .modules.utilities.path.mcptool_path import MCPToolPath

# Remove the default logger
logger.remove()

# Set the logging configuration
logger.add(os.path.join(MCPToolPath().get(), 'debug.log'),
    level='INFO',
    format='[{time} {level} - {file}, {line}] ⮞ <level>{message}</level>', 
    rotation="30 MB"
)

# Check if the files exist
MCPToolPath().check_files()

from mccolors import mcwrite, mcreplace

# Utilities
from .modules.utilities.managers.language_manager import LanguageManager as LM
from .modules.utilities.banners.banners import MCPToolBanners, InputBanners
from .modules.utilities.banners.show_banner import ShowBanner
from .modules.utilities.constants import VERSION


class MCPTool:
    __version__: str = VERSION
    
    def __init__(self, commands_folder_path: str = 'src/mcptool/modules/commands'):
        self.commands_folder_path: str = commands_folder_path
        self.commands: dict = {}

    @logger.catch
    def run(self):
        # Notify the user that the tool is starting
        logger.info(f'MCPTool v{self.__version__} is starting...')

        # Load the commands
        self.commands = self._get_commands()

        # Start the command input
        self._command_input()

    @logger.catch
    def _command_input(self) -> None:
        """
        Method to manage the command line input
        """

        ShowBanner(MCPToolBanners.BANNER_1, clear_screen=True).show()
        
        while True:
            try:
                # Get the user input
                arguments: list = input(mcreplace(InputBanners.INPUT_1)).split()

                # Check if the arguments are empty
                if len(arguments) == 0:
                    continue

                # Get the command
                command_name: str = arguments[0].lower()

                # Check if the command is exit
                if command_name == "exit":
                    break

                # Check if the command exists
                if command_name not in self.commands:
                    mcwrite(LM().get(['commands', 'invalidCommand']))
                    continue

                try:
                    # Execute the command
                    command_instance = self.commands[command_name]
                    command_instance.execute(arguments[1:])

                except KeyboardInterrupt:
                    mcwrite(LM().get(['commands', 'ctrlC']))
                    continue

            except (RuntimeError, EOFError):
                pass

            except KeyboardInterrupt:
                break

    @logger.catch
    def _get_commands(self) -> dict:
        """
        Method to get the commands

        Returns:
            dict: The commands
        """

        # Commands
        from .modules.commands.clear import Command as ClearCommand
        from .modules.commands.help import Command as HelpCommand
        from .modules.commands.discord import Command as DiscordCommand
        from .modules.commands.server import Command as ServerCommand
        from .modules.commands.uuid import Command as UUIDCommand
        from .modules.commands.ipinfo import Command as IPInfoCommand
        from .modules.commands.seeker import Command as SeekerCommand
        from .modules.commands.scan import Command as ScanCommand
        from .modules.commands.kick import Command as KickCommand
        from .modules.commands.kickall import Command as KickAllCommand
        from .modules.commands.listening import Command as ListeningCommand
        from .modules.commands.bruteauth import Command as BruteAuthCommand
        from .modules.commands.connect import Command as ConnectCommand
        from .modules.commands.proxy import Command as ProxyCommand
        from .modules.commands.rcon import Command as RconCommand
        from .modules.commands.checker import Command as CheckerCommand

        return {
            'clear': ClearCommand(),
            'help': HelpCommand(),
            'discord': DiscordCommand(),
            'server': ServerCommand(),
            'uuid': UUIDCommand(),
            'ipinfo': IPInfoCommand(),
            'seeker': SeekerCommand(),
            'scan': ScanCommand(),
            'kick': KickCommand(),
            'kickall': KickAllCommand(),
            'listening': ListeningCommand(),
            'bruteauth': BruteAuthCommand(),
            'connect': ConnectCommand(),
            'proxy': ProxyCommand(),
            'rcon': RconCommand(),
            'checker': CheckerCommand()
        }
