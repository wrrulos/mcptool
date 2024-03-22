import logging

from mccolors import mcwrite, mcreplace

from .modules.utilities.managers.language_manager import LanguageManager as LM
from .modules.utilities.commands.loader import CommandLoader


class MCPTool:
    def __init__(self, commands_folder_path: str = 'src/mcptool/modules/commands'):
        self.commands_folder_path = commands_folder_path
        self.commands: dict = {}

    def run(self):
        # Set the logging configuration
        logging.basicConfig(filename='debug.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Notify the user that the tool is starting
        logging.info(LM().get(['logger', 'starting']))

        # Load the commands
        self.commands = CommandLoader(commands_folder_path=self.commands_folder_path).get_commands()

        # Start the command input
        self._command_input()

    def _command_input(self) -> None:
        """
        Method to manage the command line input
        """

        while True:
            try:
                # arguments = input(mcreplace(LM().get(['commands', 'input']))).split()
                arguments: list = input(mcreplace('Enter a command: ')).split()

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