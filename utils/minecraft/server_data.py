import asyncio
import socket
import dns
import re

from mcstatus import JavaServer, BedrockServer
from utils.gets.get_player_uuid_color import uuid_color
from utils.checks.check_domain import check_domain
from utils.gets.get_ip_address import get_ip_address
from utils.gets.get_dns_records import get_dns_records
from utils.color.mini_messages_format import minecraft_colors


class GetDataFromMinecraftServer:
    def __init__(self, server):
        self.server = server
        self.port = None
        self.old_server = ''

    def get_information(self):
        """
        Retrieves various information from the Minecraft server.

        Returns:
            list: A list containing the following server information:
                - server_type (str): The type of server (Java or Bedrock).
                - ip_and_port (str): The IP address and port of the server.
                - motd (str): The server's Message of the Day (MOTD).
                - version (str): The server's version.
                - protocol (int): The server's protocol version.
                - connected_players (int): The number of players currently connected to the server.
                - max_player_limit (int): The maximum player limit of the server.
                - additional_info (varies): Additional information specific to the server type.
                - ms (int): The server's latency in milliseconds.

        Note:
            The format of `additional_info` varies based on the server type:
            - For Java servers:
                - mod_type (str): The type of mods installed on the server.
                - mod_list (list): A list of dictionaries representing the installed mods.
            - For Bedrock servers:
                - brand (str): The server's brand or software name.
                - map (str): The current map or world name on the server.
                - gamemode (str): The default gamemode set on the server.
        """
        port_pattern = r'^\d{1,5}$'

        try:
            if ':' in self.server:
                valid_port = re.match(port_pattern, self.server.split(':')[1])

                if not valid_port:
                    return None

                if self.server.count(':') > 1:
                    self.server = self.server.split(':', 1)[0]

            server_type, response = self._get_data(self.server)
            self.port = self._get_port(server_type) if ':' not in self.server else self.server.split(':')[1]

            if check_domain(self.server):
                self._resolve_domain()

            if server_type is None:
                return None

            ip_and_port = f'{self.server}:{self.port}' if ':' not in self.server else self.server
            protocol = response.version.protocol
            ms = round(response.latency)

            if server_type == 'Java':
                motd = response.description
                version = response.version.name
                clean_motd = self._clean_data(motd)
                clean_version = self._clean_data(version)
                connected_players = response.players.online
                max_player_limit = response.players.max
                player_list = response.players.sample
                favicon = response.favicon
                mod_info = response.raw.get('modinfo', {})
                mod_type = mod_info.get('type')
                mod_list = mod_info.get('modList', [])

                if player_list is not None:
                    texts_with_spaces = 0

                    for player in player_list:
                        if ' ' in player.name:
                            texts_with_spaces += 1

                    if texts_with_spaces >= 3:
                        players = str([f'{player.name}' for player in player_list])
                        players = players.replace('[', '').replace(']', '').replace("'", '').replace("&f&l(&500000000-0000-0000-0000-000000000000&f&l), ", '').replace("&f&l(&500000000-0000-0000-0000-000000000000&f&l)", '').replace(', ', ' ')

                    else:
                        players = str([f'&f&l{player.name} &f&l({uuid_color(player.name, player.id)}{player.id}&f&l)' for player in player_list])
                        players = players.replace('[', '').replace(']', '').replace("'", '').replace("&f&l(&500000000-0000-0000-0000-000000000000&f&l), ", '').replace("&f&l(&500000000-0000-0000-0000-000000000000&f&l)", '')

                    re.findall(
                        r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]',
                        players
                    )

                    player_list = self._clean_data(players)

                if len(mod_list) >= 1:
                    formatted_list = [f"&f&l{item['modid']} (&a&l{item['version']}&f&l)" for item in mod_list]
                    mod_list = ', '.join(formatted_list)

                return [
                    server_type,
                    ip_and_port,
                    motd,
                    version,
                    protocol,
                    connected_players,
                    max_player_limit,
                    player_list,
                    favicon,
                    mod_type,
                    mod_list,
                    ms,
                    clean_motd,
                    clean_version,
                    response.players.sample
                ]

            else:
                motd = response.motd
                version = response.version.version
                clean_motd = self._clean_data(motd)
                clean_version = self._clean_data(version)
                # brand = response.version.brand
                connected_players = response.players_online
                max_player_limit = response.players_max
                map = response.map
                gamemode = response.gamemode

                return [
                    server_type,
                    ip_and_port,
                    motd,
                    version,
                    protocol,
                    # brand,
                    connected_players,
                    max_player_limit,
                    map,
                    gamemode,
                    ms,
                    clean_motd,
                    clean_version
                ]

        except KeyboardInterrupt:
            return 'CtrlC'

    def _get_data(self, server):
        """
        Retrieves server data for the specified Minecraft server.

        Args:
            server (str): The server address or domain.

        Returns:
            tuple: A tuple containing the following information:
            - server_type (str): The type of server (Java or Bedrock).
            - response (object): An object containing the server's status information.
        """

        if ':' not in self.server and not check_domain(self.server):
            server = f'{self.server}:25565'

        try:
            java_server = JavaServer.lookup(server)
            return 'Java', java_server.status()

        except (OSError, TypeError, ValueError, IndexError, TimeoutError, asyncio.exceptions.TimeoutError, socket.gaierror, socket.timeout, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout, dns.resolver.NoNameservers):
            try:
                if ':' not in self.server and not check_domain(self.server):
                    server = f'{self.server}:19132'

                bedrock_server = BedrockServer.lookup(server)
                return 'Bedrock', bedrock_server.status()

            except (OSError, TypeError, ValueError, IndexError, TimeoutError, asyncio.exceptions.TimeoutError, socket.gaierror, socket.timeout, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout, dns.resolver.NoNameservers):
                return None, None

    def _resolve_domain(self):
        """
         Resolves the domain name of the Minecraft server and retrieves server data.

         Returns:
            tuple: A tuple containing the following information:
                - server_type (str): The type of server (Java or Bedrock).
                - response (object): An object containing the server's status information.

         Note:
             This function first tries to resolve the domain name using DNS and retrieves the IP addresses associated with it.
             Then, it iterates through the IP addresses, attempting to retrieve server data for each one using `_get_data`.
             If a valid server response is found, the server type and response are returned.
             If no valid response is found, it tries to directly get the IP address of the server using `get_ip_address`.
             If an IP address is found, it updates the `self.server` attribute and retrieves server data using `_get_data`.
             Finally, the server type and response are returned.
        """

        server = self.server

        if ':' in server:
            server = server.split(':')[0]

        ip_addresses = get_dns_records(server, 'A')

        if ip_addresses is not None and len(ip_addresses) >= 1:
            self.server = ip_addresses[0]

        else:
            ip_address = get_ip_address(server)

            if ip_address is not None:
                self.server = ip_address

            else:
                ip_addresses = get_dns_records(server, 'AAAA')

                if ip_addresses is not None and len(ip_addresses) >= 1:
                    self.server = ip_addresses[0]

    def _get_port(self, server_type):
        """
        Retrieves the port number for the Minecraft server.

        Returns:
            int: The port number of the server.

        Note:
            This function uses DNS SRV records to retrieve the port number associated with the Minecraft server.
            If an SRV record is found, the port number is returned.
            If no SRV record is found, the default Minecraft server port (25565) is returned.
        """

        hostname = f"_minecraft._tcp.{self.server}"

        try:
            answers = dns.resolver.resolve(hostname, 'SRV')
            self.server = answers[0].target
            return answers[0].port

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
            if server_type == 'Java':
                return 25565

            elif server_type == 'Bedrock':
                return 19132

            else:
                return None

    def _clean_data(self, data):
        if type(data) != str:
            data = data.raw

        data = str(data).replace('\n', '')
        data = re.sub(' +', ' ', data)
        data = minecraft_colors(data)
        return data