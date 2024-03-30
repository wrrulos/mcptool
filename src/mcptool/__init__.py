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
    rotation="50 MB"
)

from mccolors import mcwrite, mcreplace

# Utilities
from .modules.utilities.managers.language_manager import LanguageManager as LM


class MCPTool:
    __version__: str = '1.0-alpha'
    
    def __init__(self, commands_folder_path: str = 'src/mcptool/modules/commands'):
        self.commands_folder_path = commands_folder_path
        self.commands: dict = {}

    def run(self):
        # Check if the files exist
        MCPToolPath().check_files()

        # Notify the user that the tool is starting
        logger.info(LM().get(['logger', 'starting']))

        # Load the commands
        self.commands = self._get_commands()

        # Start the command input
        self._command_input()

    def _command_input(self) -> None:
        """
        Method to manage the command line input
        """
        
        print(MCPToolPath().get())
        while True:
            try:
                arguments = input(mcreplace(LM().get(['commands', 'input']))).split()

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
                    continue

            except (RuntimeError, EOFError):
                pass

            except KeyboardInterrupt:
                break

    def _get_commands(self) -> dict:
        """
        Method to get the commands

        Returns:
            dict: The commands
        """

        # Commands
        from .modules.commands.server import Command as ServerCommand
        from .modules.commands.player import Command as PlayerCommand
        from .modules.commands.ipinfo import Command as IPInfoCommand

        return {
            'server': ServerCommand(),
            'player': PlayerCommand(),
            'ipinfo': IPInfoCommand()
        }

