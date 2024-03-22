from typing import Union
from mccolors import mcwrite

from src.mcptool.utilities.minecraft.server.get_server import JavaServerData, BedrockServerData


class Messages:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_server_message(server_data: Union[JavaServerData, BedrockServerData]) -> str:
        """
        Method to get the server message
        """

        server_message: str = f'''
&4[&c&lIP:&f&lPORT&4] &f&l{server_data.ip_address}:{server_data.port}
&4[&c&lMO&f&lTD&4] &f&l{server_data.motd}
&4[&c&lVers&f&lion&4] &f&l{server_data.version}
&4[&c&lProto&f&lcol&4] &f&l{server_data.protocol}
&4[&c&lPlay&f&lers&4] &6&l{server_data.connected_players}&8&r/&6&l{server_data.max_players}'''

        if isinstance(server_data, JavaServerData):
            server_message += f'''
&4[&c&lPlayer List&4] &f&l{server_data.players}
&4[&c&lMo&f&ld&4] &d&l{server_data.mod}
&4[&c&lMo&f&lds&4] &f&l{server_data.mods}'''
            
        else:
            server_message += f'''
            '''

        server_message += f'''
&4[&c&lPi&f&lng&4] &f&l{server_data.ping}
&4[&c&lBot Out&f&lput&4] &f&l{server_data.bot_output}'''

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
