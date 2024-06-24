import re

from typing import Union
from loguru import logger

from ..text.text_utilities import TextUtilities


class JavaServerData:
    def __init__(self, ip_address: str, port: int, motd: str, original_motd: str, version: str, original_version: str, protocol: str, connected_players: str, max_players: str, players: str, player_list: list, mod: str, mods: list, favicon: Union[str, None], ping: int, bot_output: str) -> None:
        self.platform = 'Java'
        self.ip_address = ip_address
        self.port = port
        self.motd = motd
        self.original_motd = original_motd
        self.version = version
        self.original_version = original_version
        self.protocol = protocol
        self.connected_players = connected_players
        self.max_players = max_players
        self.players = players
        self.player_list = player_list
        self.mod = mod
        self.mods = mods
        self.favicon = favicon
        self.ping = ping
        self.bot_output = bot_output


class BedrockServerData:
    def __init__(self, ip_address: str, port: int, motd: str, version: str, protocol: str, connected_players: str, max_players: str, brand: str, map: str, gamemode: str, ping: int, bot_output: str) -> None:
        self.platform = 'Bedrock'
        self.ip_address = ip_address
        self.port = port
        self.motd = motd
        self.version = version
        self.protocol = protocol
        self.connected_players = connected_players
        self.max_players = max_players
        self.brand = brand
        self.map = map
        self.gamemode = gamemode
        self.ping = ping
        self.bot_output = bot_output


@logger.catch
def clean_output(output: str) -> str:
        """
        Method to clean the output

        Args:
            output (str): The output

        Returns:
            str: The cleaned output
        """

        # Remove newline characters.
        output = output.replace('\n', '')

        # Replace multiple spaces with a single space.
        output = re.sub(' +', ' ', output)

        # Replace Minecraft color codes with MiniMessage colored characters.
        output = TextUtilities.minecraft_colors(output)
        return output