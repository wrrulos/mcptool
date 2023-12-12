import httpx
import hashlib
import uuid
import dns
import asyncio
import subprocess
import re

from json import JSONDecodeError

from mcstatus_mcpt.status_response import JavaStatusResponse, BedrockStatusResponse
from src.managers.json_manager import JsonManager
from src.api.ping_as_java_and_bedrock_in_one_time import status
from src.utilities.get_utilities import GetUtilities


class JavaServerData:
    def __init__(self, platform_type, ip_port, motd, version, protocol, connected_players, max_player_limit, player_list, default_player_list, favicon, mod_type, mod_list, latency, bot_response) -> None:
        self.platform_type = platform_type
        self.ip_port = ip_port
        self.motd = motd
        self.version = version
        self.protocol = protocol
        self.connected_players = connected_players
        self.max_player_limit = max_player_limit
        self.player_list = player_list
        self.default_player_list = default_player_list
        self.favicon = favicon
        self.mod_type = mod_type
        self.mod_list = mod_list
        self.latency = latency
        self.bot_response = bot_response


class BedrockServerData:
    def __init__(self, platform_type, ip_port, motd, version, protocol, brand, connected_players, max_player_limit, map, gamemode, latency, bot_response) -> None:
        self.platform_type = platform_type
        self.ip_port = ip_port
        self.motd = motd
        self.version = version
        self.protocol = protocol
        self.brand = brand
        self.connected_players = connected_players
        self.max_player_limit = max_player_limit
        self.map = map
        self.gamemode = gamemode
        self.latency = latency
        self.bot_response = bot_response


class MinecraftServerData:
    @staticmethod
    async def get_server_data(server, bot, clean_data):
        """
        Retrieve data about a Minecraft server.

        Args:
            server (str): The address of the Minecraft server in the format 'hostname:port' or 'hostname'.

        Returns:
            JavaServerData or BedrockServerData or None: Server data if successful, None if no response or an error occurred.
        """

        # Check if the server address contains a port. If not, attempt to retrieve the port.
        if ':' not in server:
            ip_address = await MinecraftServerData.get_minecraft_ip_address(server)
            port = await MinecraftServerData.get_minecraft_server_port(server)

            if port is not None:
                server = f'{ip_address}:{port}'
            else:
                server = ip_address

        # Use the 'status' function to get server information.
        response = await status(server)

        if response is None:
            return None
        
        # Handle Java server response.
        if isinstance(response, JavaStatusResponse):
            server = server if ':' in server else f'{server}:25565'

            if bot:
                if JsonManager.get(['minecraftServerOptions', 'checkServerLoginWithABot']):
                    # Retrieve bot response for Bedrock server.
                    bot_response = await MinecraftServerData.get_bot_response(server, response.version.protocol)

                else:
                    bot_response = None

            else:
                bot_response = None

            if type(response.description) != str:
                response.description = response.description.raw

            if clean_data:
                motd = await MinecraftServerData.__clean_data(response.description)
                version = await MinecraftServerData.__clean_data(response.version.name)
                bot_response = await MinecraftServerData.__clean_data(bot_response)

            else:
                motd = response.description
                version = response.version.name

            return JavaServerData(
                'Java',
                server,
                motd,
                version,
                response.version.protocol,
                response.players.online,
                response.players.max,
                await MinecraftServerData.get_clean_list_player_names(response.players.sample),
                response.players.sample,
                response.favicon,
                response.raw.get('modinfo', {}).get('type'),
                response.raw.get('modinfo', {}).get('modList', []),
                response.latency,
                bot_response
            )
        
        # Handle Bedrock server response.
        elif isinstance(response, BedrockStatusResponse):
            server = server if ':' in server else f'{server}:19132'

            """
            if JsonManager.get(['minecraftServerOptions', 'checkServerLoginWithABot']):
                # Retrieve bot response for Bedrock server.
                bot_response = await MinecraftServerData.get_bot_response(server, response.version.protocol)

            else:
                bot_response = None"""
            
            bot_response = '&cNot compatible with Bedrock'

            if type(response.motd) != str:
                response.motd = response.motd.raw

            if clean_data:
                motd = await MinecraftServerData.__clean_data(response.motd)
                bot_response = await MinecraftServerData.__clean_data(bot_response)

            else:
                motd = response.motd
            
            return BedrockServerData(
                'Bedrock',
                server,
                motd,
                response.version.version,
                response.version.protocol,
                response.version.brand,
                response.players_online,
                response.players_max,
                response.map,
                response.gamemode,
                response.latency,
                bot_response
            )
        
        else:
            return None
        
    @staticmethod
    async def get_minecraft_server_port(server):
        """
        Retrieve the port number for the Minecraft server using SRV DNS records.

        This method asynchronously retrieves the port number of the Minecraft server by querying
        SRV (Service) DNS records associated with the given server's hostname. It constructs
        the SRV DNS query hostname using the standard Minecraft format.
        
        Args:
            server (str): The Minecraft server's hostname or domain.

        Returns:
            int or None: The port number of the Minecraft server, or None if not found.
        """
        
        # Construct the SRV DNS query hostname using the Minecraft format.
        hostname = f'_minecraft._tcp.{server}'

        try:
            # Use the dns.resolver to query SRV DNS records for the server.
            answers = dns.resolver.resolve(hostname, 'SRV')
            
            # Extract the target (server) and port information from the SRV DNS record.
            server = answers[0].target
            port = answers[0].port

            return port

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
            # Handle exceptions and return None if the SRV DNS record is not found.
            return None
        
    @staticmethod
    async def get_minecraft_ip_address(server):
        """
        Retrieve the Minecraft server's IP address using DNS records.

        This method asynchronously retrieves the IP addresses associated with the given
        server by querying DNS records of type 'A' (IPv4 addresses). If one or more IP
        addresses are found, it returns the first one.

        Args:
            server (str): The Minecraft server's address (e.g., hostname or domain).

        Returns:
            str or None: The first IPv4 address of the Minecraft server, or None if not found.
        """
        
        # Use the get_dns_records method to query 'A' records for the server.
        ip_addresses = await MinecraftServerData.get_dns_records(server, 'A')
        
        # Check if at least one IP address is found.
        if ip_addresses is not None and len(ip_addresses) >= 1:
            # Return the first IP address found.
            return ip_addresses[0]
        
    @staticmethod
    async def get_clean_list_player_names(player_list):
        """
        Get a clean list of player names with optional UUIDs for display.

        Args:
            player_list (list): List of player data.

        Returns:
            str or None: A formatted string containing player names with optional UUIDs, or None if the player list is empty.
        """

        if player_list is not None:
            texts_with_spaces = 0

            # Count the number of player names with spaces.
            for player in player_list:
                if ' ' in player.name:
                    texts_with_spaces += 1

            if texts_with_spaces >= 3:
                # If there are more than or equal to 3 player names with spaces, format without UUIDs.
                players = str([f'{player.name}' for player in player_list])
                players = players.replace('[', '').replace(']', '').replace("'", '').replace(
                    "&f&l(&500000000-0000-0000-0000-000000000000&f&l), ", '').replace(
                    "&f&l(&500000000-0000-0000-0000-000000000000&f&l)", '').replace(', ', ' ')

            else:
                # If there are fewer than 3 player names with spaces, format with UUIDs and colors.
                players = str([f'&f&l{player.name} &f&l({await MinecraftServerData.get_uuid_color(player.name, player.id)}{player.id}&f&l)' for player in player_list])
                players = players.replace('[', '').replace(']', '').replace("'", '').replace(
                    "&f&l(&500000000-0000-0000-0000-000000000000&f&l), ", '').replace(
                    "&f&l(&500000000-0000-0000-0000-000000000000&f&l)", '')

            # Use regex to find UUID patterns in the player string.
            re.findall(
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]',
                players
            )

            return players

        return None
    
    @staticmethod
    async def get_player_uuid(username):
        """
        Return the premium UUID (if possible) and non-premium UUID of the logged-in user.

        Args:
            username (str): Username

        Returns:
            str or tuple: If a premium account, returns a tuple containing both premium and non-premium UUIDs,
            otherwise returns a tuple containing None for the premium UUID and the non-premium UUID.
        """

        api = 'https://api.mojang.com/users/profiles/minecraft/'

        try:
            async with httpx.AsyncClient() as session:
                async with session.get(f'{api}{username}') as response:
                    response_json = await response.json()

                    # Extract and format the online UUID.
                    online_uuid = response_json['id']
                    online_uuid = f'{online_uuid[0:8]}-{online_uuid[8:12]}-{online_uuid[12:16]}-{online_uuid[16:20]}-{online_uuid[20:32]}'

                    # Generate the offline UUID using an MD5 hash of the username.
                    offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))

                    # Return a tuple containing the online and offline UUIDs.
                    return online_uuid, offline_uuid

        except (JSONDecodeError, KeyError):
            # Handle exceptions and return a tuple with None for the online UUID and the offline UUID.
            offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))
            return None, offline_uuid

        
    @staticmethod
    async def get_uuid_color(username, uuid):
        """
        Return whether the user's UUID is premium, non-premium, or modified.

        Args:
            username (str): Username
            uuid (str): UUID

        Returns:
            str: UUID Color ('&a' for premium, '&7' for non-premium, '&5' for modified)
        """

        # Get the online and offline UUIDs for the username.
        online_uuid, offline_uuid = await MinecraftServerData.get_player_uuid(username)

        # Check if the provided UUID matches the online UUID.
        if uuid == online_uuid:
            return '&a'  # Premium UUID color
            
        # Check if the provided UUID matches the offline UUID.
        elif uuid == offline_uuid:
            return '&7'  # Non-premium UUID color
            
        # If neither the online nor offline UUIDs match, consider it modified.
        else:
            return '&5'  # Modified UUID color
        
    @staticmethod
    async def get_bot_response(ip_port, protocol):
        """
        Retrieve the response from the bot checker script.

        Args:
            ip_port (str): The IP address and port of the server in the format 'ip:port'.
            protocol (int): The protocol version of the server.

        Returns:
            str: The response from the bot checker script.
        """

        # Split the provided 'ip_port' into separate IP and port components.
        try:
            ip, port = ip_port.split(':')

        except ValueError:
            return 'Error'

        # Construct the command to run the bot checker script.
        if JsonManager.get(["minecraftServerOptions", "proxy"]):
            command = f'node mcptool_files/scripts/checker.js {ip} {port} {protocol} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

        else:
            command = f'node mcptool_files/scripts/checker.js {ip} {port} {protocol} {len(GetUtilities.get_spaces())}'

        proxy_file = None  # You may specify a proxy file here if needed.

        if proxy_file is not None:
            command += f' {proxy_file}'

        # Create a subprocess to execute the bot checker script.
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Await the completion of the subprocess and capture its output.
        stdout, stderr = await process.communicate()
            
        if stderr:
            # Handle any potential errors from the subprocess.
            error_message = stderr.decode('utf-8')

            if 'Error: Cannot find module' in error_message:
                return 'Error (Missing NodeJS modules!)'
            
            elif 'not found' in error_message or '"node"' in error_message:
                return 'Error (NodeJS is not installed)'
            
            else:
                return 'Error'
            
        else:
            # Return the stdout (script output) as the bot response.
            output = stdout.decode('utf-8').replace('\n', '')
            output = re.sub(' +', ' ', output)
            output = MinecraftServerData.improve_bot_response(output)
            return output
        
    def get_bot_response_sync(ip_port, protocol):
        """
        Retrieve the response from the bot checker script synchronously.

        Args:
            ip_port (str): The IP address and port of the server in the format 'ip:port'.
            protocol (int): The protocol version of the server.

        Returns:
            str: The response from the bot checker script.
        """

        # Split the provided 'ip_port' into separate IP and port components.
        try:
            ip, port = ip_port.split(':')

        except ValueError:
            return 'Error'

        # Construct the command to run the bot checker script.
        if JsonManager.get(["minecraftServerOptions", "proxy"]):
            command = f'node mcptool_files/scripts/checker.js {ip} {port} {protocol} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

        else:
            command = f'node mcptool_files/scripts/checker.js {ip} {port} {protocol} {len(GetUtilities.get_spaces())}'

        proxy_file = None  # You may specify a proxy file here if needed.

        if proxy_file is not None:
            command += f' {proxy_file}'

        # Create a subprocess to execute the bot checker script.
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Capture the output and errors from the subprocess.
        stdout, stderr = process.communicate()

        if stderr:
            # Handle any potential errors from the subprocess.
            error_message = stderr.decode('utf-8')

            if 'Error: Cannot find module' in error_message:
                return 'Error (Missing NodeJS modules!)'
            
            elif 'not found' in error_message or '"node"' in error_message:
                return 'Error (NodeJS is not installed)'
            
            else:
                return 'Error'

        else:
            # Return the stdout (script output) as the bot response.
            output = stdout.decode('utf-8').replace('\n', '')
            output = re.sub(' +', ' ', output)
            output = MinecraftServerData.improve_bot_response(output)
            return output
        
    @staticmethod
    async def get_dns_records(hostname, record_type='All'):
        """
        Retrieve DNS records for the specified hostname.

        Args:
            hostname (str): The hostname for which DNS records are to be retrieved.
            record_type (str, optional): The type of DNS record to retrieve. Default is 'All'.

        Returns:
            list[str] or None: A list of DNS records for the hostname, or None if there was an error.
        """

        try:
            # Initialize an empty list to store DNS records.
            records_list = []
            
            # Use the dns.resolver to query DNS records for the specified hostname and type.
            records = dns.resolver.resolve(hostname, record_type)

            # Iterate through the DNS records and add them to the list.
            for record in records:
                records_list.append(record.to_text())

            return records_list

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
            # Handle exceptions and return None if an error occurs.
            return None
        
    @staticmethod
    def improve_bot_response(bot_response):
        """
        Improve the bot response by replacing specific messages with more informative ones.

        Args:
            bot_response (str): The original bot response message.

        Returns:
            str: The improved bot response with replaced messages.
        """

        # Define a dictionary of messages to replace and their replacements.
        messages = {
            'http//Minecraft.netMinecraft.net': 'http//Minecraft.net',
            'multiplayer.disconnect.invalid_public_key_signature': '§cInvalid signature for profile public key',
            'multiplayer.disconnect.banned_ip.reasonwith': '§cYou are IP banned for the following reason: ',
            'multiplayer.disconnect.banned.reasonwith': '§cYou are banned for the following reason: ',
            'multiplayer.disconnect.incompatiblewith': '§cIncompatible versions: ',
            'multiplayer.disconnect.unverified_username': '§6Premium Server',
            'multiplayer.disconnect.not_whitelisted': '§bWhitelist',
            'multiplayer.disconnect.incompatible': '§cVersion Incompatible',
            'This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details.': '§dForge Server',
            'This server has mods that require Forge to be installed on the client. Contact your server admin for more details.': '§dForge Server',
            'If you wish to use IP forwarding, please enable it in your BungeeCord config as well!': '§cVulnerable to Bungee Exploit',
            'Unable to authenticate - no data was forwarded by the proxy.': '&cBungeeguard',
            'You are not whitelisted on this server!': '§bWhitelist',
            'You have to join through the proxy.': '&cIPWhitelist',
            'Not authenticated with Minecraft.net': '§6Premium Server',
            'disconnect.genericReasonwith': '§c',
        }

        # Iterate through the messages and replace them in the bot_response.
        for message, replacement in messages.items():
            bot_response = bot_response.replace(message, replacement)
        
        return bot_response

    @staticmethod
    async def __clean_data(data):
        """
        Clean and format data by removing extra spaces and newline characters.

        Args:
            data (str or dict): The data to be cleaned.

        Returns:
            str: The cleaned and formatted data.
        """

        if data is not None:
            # Remove newline characters.
            data = str(data).replace('\n', '')

            # Replace multiple spaces with a single space.
            data = re.sub(' +', ' ', data)
            return data
        
        return None
