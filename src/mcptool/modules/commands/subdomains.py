import socket
import time
import os

from loguru import logger
from mccolors import mcwrite

from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'subdomains'
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
        
        if not ValidateArgument.is_domain(arguments[0]):
            mcwrite(LM().get(['errors', 'invalidDomain']))
            return False
        
        if not os.path.exists(arguments[1]):
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
        
        domain: str = arguments[0]
        file: str = arguments[1]
        subdomains: int = 0  # Counter for the subdomains found

        # Read the file
        with open(file, 'r') as f:
            subdomain_list: list = f.readlines() 

        if len(subdomain_list) == 0:
            mcwrite(LM().get(['errors', 'subdomainsFileEmpty']))
            return

        mcwrite(LM().get(['commands', self.name, 'wordlist'])
            .replace('%file%', file)
            .replace('%subdomains%', str(len(subdomain_list)))
        )
        time.sleep(0.5)
        mcwrite(LM().get(['commands', self.name, 'gettingSubdomains']))

        # Check the lines
        for subdomain in subdomain_list:
            try:
                host = f'{subdomain}.{domain}'
                ip = socket.gethostbyname(host)
                
                # Display information about the resolved subdomain.
                mcwrite(LM().get(['commands', self.name, 'subdomainFound'])
                    .replace('%subdomain%', host)
                    .replace('%ip%', ip)
                )
                    
                # Increment the subdomains counter.
                subdomains += 1

            except socket.gaierror:
                continue

        if subdomains == 0:
            mcwrite(LM().get(['commands', self.name, 'noSubdomains'])
                .replace('%file%', file)
            )
            return
        
        mcwrite(LM().get(['commands', self.name, 'subdomainsFound'])
            .replace('%subdomains%', str(subdomains))
        )
