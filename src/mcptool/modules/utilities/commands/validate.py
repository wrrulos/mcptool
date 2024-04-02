from mccolors import mcwrite

from ..managers.language_manager import LanguageManager as LM


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
    def is_domain(domain: str) -> bool:
        """
        Method to validate if a string is a domain
        """

        if domain.count('.') < 1:
            return False

        # Split the domain into parts
        domain_parts = domain.split('.')

        # Check if each part is alphanumeric
        for part in domain_parts:
            if not part.isalnum():
                return False

        return True
    
    @staticmethod
    def is_ip_address(ip: str) -> bool:
        """
        Method to validate if a string is an IP address
        """

        ip_parts: list = ip.split('.')

        if len(ip_parts) != 4:
            return False

        for part in ip_parts:
            try:
                part: int = int(part)

                if part < 0 or part > 255:
                    return False
                
            except ValueError:
                return False

        return True
    
    @staticmethod
    def is_ip_and_port(ip: str) -> bool:
        """
        Method to validate if a string is an IP and port
        """

        if ':' not in ip:
            return False

        ip_parts: list = ip.split(':')

        if len(ip_parts) != 2:
            return False

        ip_address: str = ip_parts[0]
        port: str = ip_parts[1]

        if not ip_address or not port:
            return False

        try:
            port: int = int(port)

            if port < 0 or port > 65535:
                return False
            
        except ValueError:
            return False

        ip_parts: list = ip_address.split('.')

        if len(ip_parts) != 4:
            return False

        for part in ip_parts:
            try:
                part: int = int(part)

                if part < 0 or part > 255:
                    return False
                
            except ValueError:
                return False

        return True

    @staticmethod
    def is_seeker_subcommand(subcommand: str) -> bool:
        """
        Method to validate if a string is a seeker subcommand
        """

        if subcommand not in ['token', 'servers']:
            return False

        return True
