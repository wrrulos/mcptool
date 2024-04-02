from typing import Union
from mccolors import mcwrite

from .get_server import JavaServerData, BedrockServerData
from ...managers.language_manager import LanguageManager as LM


class Messages:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_server_message(server_data: Union[JavaServerData, BedrockServerData]) -> str:
        """
        Method to get the server message
        """

        server_message: str = f'''
{LM().get(['commands', 'server', 'ip_and_port']).replace('%ip%', server_data.ip_address).replace('%port%', str(server_data.port))}
{LM().get(['commands', 'server', 'motd']).replace('%motd%', server_data.motd)}
{LM().get(['commands', 'server', 'version']).replace('%version%', server_data.version)}
{LM().get(['commands', 'server', 'protocol']).replace('%protocol%', str(server_data.protocol))}
{LM().get(['commands', 'server', 'connected']).replace('%connectedPlayers%', str(server_data.connected_players)).replace('%maxPlayers%', str(server_data.max_players))}'''

        if isinstance(server_data, JavaServerData):
            server_message += f'''
{LM().get(['commands', 'server', 'playerList']).replace('%playerList%', server_data.players)}'''
            
            if server_data.mod:
                server_message += f'''
{LM().get(['commands', 'server', 'mod']).replace('%mod%', server_data.mod)}
{LM().get(['commands', 'server', 'modList']).replace('%modList%', str(server_data.mods))}'''
            
        else:
            server_message += f'''
            '''

        server_message += f'''
{LM().get(['commands', 'server', 'ping']).replace('%ping%', str(server_data.ping))}
{LM().get(['commands', 'server', 'bot']).replace('%bot%', str(server_data.bot_output))}'''

        return server_message


class ShowMinecraftServer:
    def __init__(self) -> None:
        pass

    @staticmethod
    def show(server_data: Union[JavaServerData, BedrockServerData]) -> None:
        """
        Method to show the server data
        """

        server_message: str = Messages.get_server_message(server_data)
        mcwrite(server_message)
