import importlib.util
import inspect
import os

from mccolors import mcwrite, mcreplace

from app.logger import Logger
from app.utilities.managers.language_manager import LanguageManager as LM


class MCPTool:
    def __init__(self) -> None:
        self.logger = Logger()
        self.commands_folder_path = "src/app/commands"
        self.commands = {}

    def start(self):
        """
        Method to start MCPTool
        """
        print("Starting MCPTool")

        # Load the commands
        self.load_commands()

        # Start the command input
        self.command_input()

    def load_commands(self):
        """
        Method to load the commands
        """

        # Get the files in the commands folder
        commands_files = os.listdir(self.commands_folder_path)

        for file_name in commands_files:
            if not file_name.endswith('.py'):
                continue

            if file_name == '__init__.py':
                continue
            
            # # Get the module name without the extension
            module_name = os.path.splitext(file_name)[0]

            # Create a module specification
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.commands_folder_path, file_name))
            
            # Load the module
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for item_name in dir(module):
                # Get the item from the module
                item = getattr(module, item_name)

                # Check if the item is a valid command class
                if inspect.isclass(item) and hasattr(item, 'execute'):
                    # Instantiate the command class
                    command_instance = item()

                    # Add the command instance to the commands dictionary
                    self.commands[command_instance.name] = command_instance

    def command_input(self):
        """
        Method to manage the command line input
        """
        
        while True:
            try:
                arguments = input(mcreplace(LM().get(['commands', 'input']))).split()

                if len(arguments) == 0:
                    continue

                # Get the command
                command_name = arguments[0].lower()

                if command_name == "exit":
                    break

                if command_name not in self.commands:
                    mcwrite(LM().get(['commands', 'invalidCommand']))
                    continue

                # Execute the command
                command_instance = self.commands[command_name]
                command_instance.execute(arguments[1:])
 
            except (RuntimeError, EOFError):
                pass

            except KeyboardInterrupt:
                break

    def manage_command(self, command, arguments):
        """
        Method to manage the commands
        """
        pass