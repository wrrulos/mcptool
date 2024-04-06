import webbrowser
import threading
import time

from ..managers.settings_manager import SettingsManager as SM
from ..managers.language_manager import LanguageManager as LM
from mccolors import mcwrite
from loguru import logger


class SeekerToken:
    @logger.catch
    @staticmethod
    def get_token() -> None:
        """
        Method to get the token from the user 
        and save it in the settings
        """

        TOKEN: str = ''
        ERROR: bool = False

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
            nonlocal ERROR

            try:
                server = HTTPServer(('localhost', 7637), TokenHandler)

            except OSError:
                mcwrite(LM().get(['commands', 'seeker', 'restart']))
                ERROR = True
                token_received.set()
                return

            server.serve_forever()

        # Start the server in a new thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        time.sleep(1)

        if not ERROR:
            # Open the browser to get the token
            webbrowser.open(SM().get(['endpoints', 'seeker']))

        # Wait for the token 
        token_received.wait()
  
        return TOKEN
        
        # Save the token in the settings
        self.token = TOKEN
        SM().set(key='seekerToken', value=self.token)
