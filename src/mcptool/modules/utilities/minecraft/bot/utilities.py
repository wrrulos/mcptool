import random

from loguru import logger

from ...path.mcptool_path import MCPToolPath


class BotUtilities:
    @logger.catch
    @staticmethod
    def get_bot_username() -> str:
        """
        Method to get the bot username

        Returns:
            str: The bot username
        """

        # Get the path of the MCPTool folder
        path: str = MCPToolPath().get()

        try:
            # Read the bot username from the file
            with open(f'{path}/txt/bot_username.txt', 'r') as file:
                lines = file.readlines()
                return random.choice(lines).strip()

        except FileNotFoundError:
            return 'MCPToolBot'
        
    @logger.catch
    @staticmethod
    def get_bot_color_response(response: str) -> str:
        """
        Method to get the color response for the bot

        Args:
            response (str): The response to get the color for

        Returns:
            str: The color response for the bot
        """
        
        # If the bot connected to the server
        if response == 'Connected':
            return '&a&lConnected'
        
        # If the bot failed to connect to the server
        messages: dict = {
            'http//Minecraft.netMinecraft.net': 'http//Minecraft.net',
            'multiplayer.disconnect.invalid_public_key_signature': '§cInvalid signature for profile public key',
            'multiplayer.disconnect.banned_ip.reasonwith': '§cYou are IP banned for the following reason: ',
            'multiplayer.disconnect.banned.reasonwith': '§cYou are banned for the following reason: ',
            'multiplayer.disconnect.incompatiblewith': '§cIncompatible versions: ',
            'multiplayer.disconnect.unverified_username': '§6§lServer in premium mode',
            'multiplayer.disconnect.not_whitelisted': '§bWhitelist',
            'multiplayer.disconnect.incompatible': '§cVersion Incompatible',
            'This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details.': '§dForge Server',
            'This server has mods that require Forge to be installed on the client. Contact your server admin for more details.': '§dForge Server',
            'If you wish to use IP forwarding, please enable it in your BungeeCord config as well!': '§cVulnerable to Bungee Exploit',
            'Unable to authenticate - no data was forwarded by the proxy.': '&cBungeeguard',
            'You are not whitelisted on this server!': '§bWhitelist',
            'You have to join through the proxy.': '&cIPWhitelist',
            'Not authenticated with Minecraft.net': '§6§lServer in premium mode',
            'disconnect.genericReasonwith': '§c',
        }

        # Iterate through the messages and replace them in the bot_response.
        for message, replacement in messages.items():
            response = response.replace(message, replacement)

        return response
