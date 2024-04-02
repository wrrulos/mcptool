import threading
import webbrowser

from typing import Union
from mccolors import mcwrite
from loguru import logger

from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.managers.settings_manager import SettingsManager as SM
from ..utilities.commands.validate import ValidateArgument
from ..utilities.input.get import GetInput


class Command:
    def __init__(self):
        self.name: str = 'seeker'
        self.token: Union[str, None] = None
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]

    def validate_arguments(self, arguments: list) -> bool:
        """
        Method to validate the arguments

        Args:
            arguments (list): The arguments to validate

        Returns:
            bool: True if the arguments are valid, False otherwise
        """

        validate = ValidateArgument(command_name=self.name, command_arguments=self.arguments, user_arguments=arguments)

        if not validate.validate_arguments_length():
            return False
        
        if not ValidateArgument.is_seeker_subcommand(arguments[0]):
            print('invalid sub command')
            return False
        
        return True

    def execute(self, arguments: list) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        # Validate the arguments
        if not self.validate_arguments(arguments):
            return
        
        if arguments[0] == 'token':
            self._get_token()

    @logger.catch
    def _get_token(self) -> None:
        """
        Method to get the token from the user 
        and save it in the settings
        """

        TOKEN: str = ''

        # Check if the endpoint is valid
        if SM().get(['endpoints', 'seeker']) is None:
            mcwrite(LM().get(['errors', 'invalidEndpoint']))
            logger.error(LM().get(['logger', 'seeker', 'invalidEndpoint']))
            return

        # Event to indicate that the token has been received
        token_received: threading.Event = threading.Event()

        # Print the message to get the token
        mcwrite(LM().get(['commands', 'seeker', 'gettingToken']))

        # Function to start the server
        def start_server():
            from http.server import BaseHTTPRequestHandler, HTTPServer

            class TokenHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    nonlocal TOKEN
                    
                    if '?api_key=' in self.path:
                        # Get the token
                        TOKEN = self.path.split('=')[1]

                        # Notify the user that the token has been obtained
                        mcwrite(LM().get(['commands', 'seeker', 'tokenObtained']))
                        logger.info(LM().get(['logger', 'seeker', 'tokenObtained']))

                        # Activate the event
                        token_received.set()

                        # Close the server
                        server.shutdown()

            # Start the server
            global server

            try:
                server = HTTPServer(('localhost', 7637), TokenHandler)

            except OSError:
                mcwrite(LM().get(['commands', 'seeker', 'restart']))
                token_received.set()

            server.serve_forever()

        # Start the server in a new thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        # Open the browser to get the token
        webbrowser.open(SM().get(['endpoints', 'seeker']))

        # Wait for the token 
        token_received.wait()
  
        if TOKEN == '':
            return
        
        # Save the token in the settings
        self.token = TOKEN
        SM().set(key='seekerToken', value=self.token)
