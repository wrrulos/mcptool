import inspect
import os

from importlib.util import spec_from_file_location, module_from_spec
from importlib.machinery import ModuleSpec
from mccolors import mcwrite, mcreplace
from typing import Union, Any
from types import ModuleType

from .logger import Logger
from .utilities.managers.language_manager import LanguageManager as LM


class MCPTool:
    def __init__(self, commands_folder_path: str = 'src/mcptool/commands'):
        self.logger = Logger()
        self.commands_folder_path = commands_folder_path
        self.commands: dict = {}

    def run(self):
        # Load the commands
        self._load_commands()

        # Start the command input
        self._command_input()

    def _load_commands(self) -> None:
        """
        Method to load the commands
        """

        # Check if the commands folder exists
        if not os.path.exists(self.commands_folder_path):
            raise Exception('The commands folder does not exist')

        # Get the files in the commands folder
        commands_files: list = os.listdir(self.commands_folder_path)

        # Check if there are any files in the commands folder
        if len(commands_files) == 0:
            raise Exception('The commands folder is empty')

        # Iterate over the files in the commands folder
        for file_name in commands_files:
            if not file_name.endswith('.py'):
                continue

            if file_name == '__init__.py':
                continue

            # Get the module name without the extension
            module_name: str = os.path.splitext(file_name)[0]

            # Create a module specification
            spec: Union[ModuleSpec, None] = spec_from_file_location(module_name,
                                                                    os.path.join(
                                                                        self.commands_folder_path,
                                                                        file_name))

            # Check if the module specification is None
            if spec is None:
                continue

            # Load the module
            module: ModuleType = module_from_spec(spec)

            # Check if the loader is None
            if spec.loader is None:
                continue

            spec.loader.exec_module(module)

            for item_name in dir(module):
                # Get the item from the module
                item: Any = getattr(module, item_name)

                # Check if the item is a valid command class
                if inspect.isclass(item) and hasattr(item, 'execute'):
                    # Instantiate the command class
                    command_instance = item()

                    # Add the command instance to the commands dictionary
                    self.commands[command_instance.name] = command_instance

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
