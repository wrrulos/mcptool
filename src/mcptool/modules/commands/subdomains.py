import threading
import socket
import time
import os

from loguru import logger
from mccolors import mcwrite

from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.managers.settings_manager import SettingsManager as SM
from ..utilities.commands.validate import ValidateArgument


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'subdomains'
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]
        self.servers_found: int = 0
        self.subdomain_found_message: str = LM().get(['commands', self.name, 'subdomainFound'])
        self.first_subdomain_found: bool = False
        self.stopped: bool = False

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
        
        if not self.validate_arguments(arguments):
            return

        domain: str = arguments[0]
        file_path: str = arguments[1]
        subdomains_found: int = 0
        results: list = []
        self.first_subdomain_found = False

        try:
            num_threads: int = int(SM().get('subdomains_threads'))

        except ValueError:
            logger.warning(f'Invalid value for subdomains_threads. Using default value (500)')
            num_threads: int = 500

        with open(file_path, 'r') as file:
            subdomain_list = [line.strip() for line in file]

        if len(subdomain_list) == 0:
            mcwrite(LM().get(['errors', 'subdomainsFileEmpty']))
            return
        
        mcwrite(LM().get(['commands', self.name, 'wordlist'])
            .replace('%file%', file_path)
            .replace('%subdomains%', str(len(subdomain_list)))
        )
        time.sleep(0.5)
        mcwrite(LM().get(['commands', self.name, 'gettingSubdomains']))

        # Check if the number of threads is greater than the number of subdomains
        if len(subdomain_list) < num_threads:
            num_threads = len(subdomain_list)

        # Divide the subdomains into chunks
        chunk_size = len(subdomain_list) // num_threads
        chunks = [subdomain_list[i:i+chunk_size] for i in range(0, len(subdomain_list), chunk_size)]

        # Create the threads
        threads: list = []

        try:
            # Scan the subdomains
            for chunk in chunks:
                thread = threading.Thread(target=self._scan_chunk, args=(domain, chunk, results))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finishs
            for thread in threads:
                thread.join()
                
            if subdomains_found == 0:
                mcwrite(LM().get(['commands', self.name, 'noSubdomains'])
                    .replace('%file%', file_path)
                )
                
            else:
                mcwrite(LM().get(['commands', self.name, 'subdomainsFound'])
                    .replace('%subdomains%', str(subdomains_found))
                )

        except KeyboardInterrupt:
            # Kill all threads
            self.stopped = True


    @logger.catch
    def _scan_subdomain(self, domain: str, subdomain: str, results: list) -> None:
        """
        Method to scan a subdomain. 
        If the subdomain is valid, it will be added to the results list

        Args:
            domain (str): The domain
            subdomain (str): The subdomain
            results (list): The results list
        """

        try:
            host: str = f'{subdomain}.{domain}'
            ip: str = socket.gethostbyname(host)

            if not self.first_subdomain_found:
                print('')
                self.first_subdomain_found = True

            mcwrite(self.subdomain_found_message
                .replace('%subdomain%', f'{subdomain}.{domain}')
                .replace('%ip%', ip)
            )
            #results.append((host, ip))

        except (socket.gaierror, UnicodeError):
            pass

    @logger.catch
    def _scan_chunk(self, domain: str, chunk: list, results: list) -> None:
        """
        Method to scan a chunk of subdomains.

        Args:
            domain (str): The domain
            chunk (list): The chunk of subdomains
            results (list): Results list to store the valid subdomains
        """

        for subdomain in chunk:
            if self.stopped:
                break
            
            self._scan_subdomain(domain, subdomain, results)
