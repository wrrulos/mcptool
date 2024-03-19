from mccolors import mcwrite

from src.mcptool.utilities.managers.language_manager import LanguageManager as LM


class ValidateArgument:
    def __init__(self, command_name: str, command_arguments: list, user_arguments: list) -> None:
        self.command_name: str = command_name
        self.command_arguments: list = command_arguments
        self.user_arguments: list = user_arguments

    def validate_arguments_length(self) -> bool:
        """
        Method to validate the arguments length
        """

        for i in range(0, len(self.command_arguments)):
            try:
                self.user_arguments[i]

            except IndexError:
                error_message: str = LM().get(['commands', 'missingArguments'])
                arguments_message: str = ''

                for argument_valid in self.command_arguments[:i]:
                    arguments_message += f'&a{argument_valid} '

                for argument_invalid in self.command_arguments[i:]:
                    arguments_message += f'&c&n{argument_invalid}&r '

                # Add the name of the command
                error_message = error_message.replace('%command%', self.command_name)

                # Add th arguments
                error_message = error_message.replace('%arguments%', arguments_message)
                
                # Print the error message
                mcwrite(error_message)
                return False
        
        return True
    
    @staticmethod
    def 