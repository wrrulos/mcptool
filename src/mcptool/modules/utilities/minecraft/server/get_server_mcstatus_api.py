import requests

from typing import Union
from loguru import logger

from ..bot.server_response import BotServerResponse
from ..bot.utilities import BotUtilities
from . import JavaServerData, BedrockServerData, clean_output


class MCStatusIOAPI:
    def __init__(self, target: str, bot: bool = True) -> None:
        self.target = target
        self.bot = bot
        self.java_endpoint: str = 'https://api.mcstatus.io/v2/status/java/'
        self.bedrock_endpoint: str = 'https://api.mcstatus.io/v2/status/bedrock/'

    @logger.catch
    def get(self) -> Union[JavaServerData, BedrockServerData, None]:
        """
        Method to get the server data from the MCStatus.io API.

        Returns:
            Union[JavaServerData, BedrockServerData, None]: The server data if the server is online, otherwise None
        """

        data: Union[JavaServerData, None] = self._send_java_request()

        if data is None:
            data: Union[BedrockServerData, None] = self._send_bedrock_request()

        # If the data is still None, return None
        if data is None:
            return None

        return data

    @logger.catch
    def _send_java_request(self) -> Union[JavaServerData, None]:
        """
        Method to send the request to the MCStatus.io API.

        Returns:
            Union[JavaServerData, None]: The server data if the server is online, otherwise None
        """

        response: requests.Response = requests.get(f'{self.java_endpoint}{self.target}')

        if response.status_code != 200:
            return None

        data: Union[JavaServerData, None] = self._convert_data(data=response.json(), server_type='java')
        return data

    @logger.catch
    def _send_bedrock_request(self) -> Union[BedrockServerData, None]:
        """
        Method to send the request to the MCStatus.io API.

        Returns:
            Union[BedrockServerData, None]: The server data if the server is online, otherwise None
        """

        response: requests.Response = requests.get(f'{self.bedrock_endpoint}{self.target}')

        if response.status_code != 200:
            return None

        data: Union[BedrockServerData, None] = self._convert_data(data=response.json(), server_type='bedrock')
        return data

    @logger.catch
    def _convert_data(self, data: dict, server_type: str) -> Union[JavaServerData, None]:
        """
        Method to convert the data to a JavaServerData object.

        Args:
            data (dict): The data
            server_type (str): The server type (Java or Bedrock)

        Returns:
            Union[JavaServerData, None]: The JavaServerData object if the server is online, otherwise None
        """

        player_list: list = []
        players_str: Union[str, None] = None

        if not data['online']:
            return None

        if server_type == 'java':
            if data['players']['list'] is not None:
                player_list = [{'name_clean': player['name_clean'], 'uuid': player['uuid']} for player in data['players']['list']]

                if len(player_list) > 0:
                    players = self._get_players(player_list)
                    players_str: str = ', '.join(players)

                ip_address: str = data['ip_address']
                port: int = data['srv_record']['port'] if data['srv_record'] is not None else data['port']
                motd: str = clean_output(data['motd']['raw'])
                original_motd: str = data['motd']['raw']
                version: str = clean_output(data['version']['name_raw'])
                original_version: str = data['version']['name_raw']
                protocol: str = data['version']['protocol']
                connected_players: str = data['players']['online']
                max_players: str = data['players']['max']
                players: str = players_str
                player_list: list = data['players']['list']
                mod: Union[str, None] = None
                mods: list = []
                favicon: Union[str, None] = data['icon']
                ping: Union[int, None] = None

                if self.bot:
                    # Get the bot output
                    bot_output: str = clean_output(BotServerResponse(ip_address, port, protocol).get_response())

                    # Get the bot color response
                    bot_output = BotUtilities.get_bot_color_response(bot_output)

                else:
                    bot_output: str = ''

                return JavaServerData(
                    ip_address=ip_address,
                    port=port,
                    motd=motd,
                    original_motd=original_motd,
                    version=version,
                    original_version=original_version,
                    protocol=protocol,
                    connected_players=connected_players,
                    max_players=max_players,
                    players=players,
                    player_list=player_list,
                    mod=mod,
                    mods=mods,
                    favicon=favicon,
                    ping=ping,
                    bot_output=bot_output
                )

        if server_type == 'bedrock':
            bot_output: str = '&c&lIncompatible'
            ip_address: str = data['ip_address']
            port: int = data['port']
            motd: str = clean_output(data['motd']['raw'])
            version: str = clean_output(data['version']['name'])
            protocol: str = data['version']['protocol']
            connected_players: str = data['players']['online']
            max_players: str = data['players']['max']
            brand: str = None
            map: Union[str, None] = None
            gamemode: Union[str, None] = data['gamemode']
            ping: Union[int, None] = None

            return BedrockServerData(
                ip_address=ip_address,
                port=port,
                motd=motd,
                version=version,
                protocol=protocol,
                connected_players=connected_players,
                max_players=max_players,
                brand=brand,
                map=map,
                gamemode=gamemode,
                ping=ping,
                bot_output=bot_output
            )

        return None

    @logger.catch
    def _get_players(self, players: Union[list, None]) -> list:
        """
        Method to get the players from the player list

        Args:
            players (Union[list, None]): The player list

        Returns:
            list: The list of players
        """

        return [player['name_clean'] for player in players] if players is not None else []
