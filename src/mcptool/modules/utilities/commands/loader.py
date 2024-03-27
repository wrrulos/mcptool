import os
import inspect
import logging

from importlib.util import spec_from_file_location, module_from_spec
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import Union, Any

from ..managers.language_manager import LanguageManager as LM


class CommandLoader:
    def __init__(self, commands_folder_path: str):
        self.commands_folder_path = commands_folder_path
        self.commands: dict = {}
    
    def get_commands(self) -> dict:
        """
        Method to get the commands

        Returns:
            dict: The commands dictionary with the command name 
            as the key and the command instance as the value
        """

        # Load the commands
        logging.info(LM().get(['logger', 'loadingCommands']))
        self._load_commands()

        # Return the commands
        logging.info(LM().get(['logger', 'commandsLoaded']))
        return self.commands
    
    def _load_commands(self) -> None:
        """
        Method to load the commands
        """

        # Check if the commands folder exists
        if not os.path.exists(self.commands_folder_path):
            logging.error(LM().get(['logger', 'commandsFolderDoesNotExist']))
            raise Exception('The commands folder does not exist')

        # Get the files in the commands folder
        commands_files: list = os.listdir(self.commands_folder_path)

        # Check if there are any files in the commands folder
        if len(commands_files) == 0:
            logging.error(LM().get(['logger', 'commandsFolderIsEmpty']))
            raise Exception('The commands folder is empty')

        # Iterate over the files in the commands folder
        for file_name in commands_files:
            if not file_name.endswith('.py'):
                continue

            if file_name == '__init__.py':
                continue

            try:
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
            
            except TypeError:
                logging.error(LM().get(['logger', 'commandsArgumentMissing']).replace('%command%', file_name))
                continue