import webbrowser
import requests
import threading
import time

from mccolors import mcwrite
from typing import Union
from loguru import logger
from easyjsonpy import get_config_value, set_config_value

from ..managers.language_utils import LanguageUtils as LM
from ..input.get import GetInput


class SeekerUtilities:
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
        if get_config_value('endpoints.seeker') is None:
            mcwrite(LM.get('errors.invalidEndpoint'))
            logger.error(f'Invalid endpoint for seeker: {get_config_value("endpoints.seeker")}')
            return

        # Event to indicate that the token has been received
        token_received: threading.Event = threading.Event()

        # Print the message to get the token
        mcwrite(LM.get('commands.seeker.token.gettingToken'))

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
                        mcwrite(LM.get('commands.seeker.token.tokenObtained'))
                        logger.info(f'Token obtained from the seeker')

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
                mcwrite(LM.get('commands.seeker.token.restart'))
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
            webbrowser.open(get_config_value('endpoints.seeker'))

        # Wait for the token
        token_received.wait()
        return TOKEN

    @logger.catch
    @staticmethod
    def get_servers(token: str) -> dict:
        """
        Method to get the servers from the seeker API

        Args:
            token (str): The seeker token

        Returns:
            dict: The servers from the seeker API
        """

        url: str = f"{get_config_value('endpoints.seekerAPI')}/servers"

        # Search options
        country_code: Union[str, None] = None
        cracked: Union[bool, None] = None
        description: Union[str, None] = None
        only_bungeespoofable: Union[bool, None] = None
        protocol: Union[int, None] = None
        online_players: Union[int, None] = None

        # Ask the user if they want to filter the servers
        filter: tuple = GetInput(LM.get('commands.seeker.servers.filterByData'), 'boolean').get_input()

        # If the user wants to filter the servers
        if filter[0]:
            # Filter by country code
            filter_country_code: tuple = GetInput(LM.get('commands.seeker.servers.filterByCountryCode'), 'boolean').get_input()

            if filter_country_code[0]:
                country_code = GetInput(LM.get('commands.seeker.servers.filterByCountryCodeText'), 'country_code').get_input()

            # Filter by cracked servers
            filter_cracked: tuple = GetInput(LM.get('commands.seeker.servers.filterByCracked'), 'boolean').get_input()
            cracked = filter_cracked[0]

            # Filter by description
            filter_description: tuple = GetInput(LM.get('commands.seeker.servers.filterByDescription'), 'boolean').get_input()

            if filter_description[0]:
                description = GetInput(LM.get('commands.seeker.servers.filterByDescriptionText'), 'string').get_input()

            # Filter by only bungeespoofable
            filter_only_bungeespoofable: tuple = GetInput(LM.get('commands.seeker.servers.filterByOnlyBungeespoofable'), 'boolean').get_input()
            only_bungeespoofable = filter_only_bungeespoofable[0]

            # Filter by protocol version
            filter_protocol: tuple = GetInput(LM.get('commands.seeker.servers.filterByProtocol'), 'boolean').get_input()

            if filter_protocol[0]:
                protocol = GetInput(LM.get('commands.seeker.servers.filterByProtocolText'), 'integer').get_input()

            # Filter by online players amount
            filter_online_players: tuple = GetInput(LM.get('commands.seeker.servers.filterByOnlinePlayers'), 'boolean').get_input()

            if filter_online_players[0]:
                online_players = GetInput(LM.get('commands.seeker.servers.filterByOnlinePlayersText'), 'integer').get_input()

        headers: dict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        data: dict = {
            'api_key': token
        }

        if country_code is not None:
            data['country_code'] = country_code[0]

        if cracked is not None and cracked:
            data['cracked'] = cracked

        if description is not None:
            data['description'] = description[0]

        if only_bungeespoofable is not None and only_bungeespoofable:
            data['only_bungeespoofable'] = only_bungeespoofable

        if protocol is not None:
            data['protocol'] = protocol[0]

        if online_players is not None:
            data['online_players'] = [online_players[0], 'inf']

        try:
            logger.info(f'''
Getting servers from the seeker API...

 ↪ URL: {url}
 ↪ Headers: {headers}
 ↪ Data: {data}''')

            mcwrite(LM.get('commands.seeker.servers.sendingRequest'))
            response = requests.post(url, headers=headers, json=data)

        except (requests.ConnectionError, requests.Timeout) as e:
            mcwrite(LM.get('errors.endpointConnectionError'))
            logger.warning(f'Error connecting to the endpoint: {url} - {data} - {e}')
            return {}

        except Exception as e:
            mcwrite(LM.get('errors.endpointConnectionError'))
            logger.error(f'Error getting the servers from the seeker API: {e}')
            return {}

        if response.status_code != 200:
            # Check if the token is invalid
            if 'error' in response.json():
                if 'Invalid api_key' in response.json()['error']:
                    mcwrite(LM.get('commands.seeker.token.invalidToken'))
                    logger.error(f'Invalid token: {token}')
                    return {}

            # If the token is valid and there is an error
            mcwrite(LM.get('errors.endpointConnectionError'))
            logger.error(f'Error getting the servers from the seeker API (Status code: {response.status_code}): {response.json()}')
            return {}

        if 'data' not in response.json():
            logger.error(f'No data in the response: {response.json()}')
            return {}

        return response.json()['data']

    @logger.catch
    def _valid_token(self, token: str) -> bool:
        """
        Check if seeker token is valid

        Returns:
            bool: True if is valid
        """

        url: str = f"{get_config_value('endpoints.seekerAPI')}/server_info"

        headers: dict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        data: dict = {
            "ip": "127.0.0.1",
            "port": 25565,
            'api_key': token
        }

        try:
            response: requests.Response = requests.post(url, headers=headers, json=data)

            if response != 200:
                return False

            return True

        except (requests.ConnectionError, requests.Timeout) as e:
            mcwrite(LM.get('errors.endpointConnectionError'))
            logger.warning(f'Error connecting to the endpoint: {url} - {data} - {e}')
            return False
