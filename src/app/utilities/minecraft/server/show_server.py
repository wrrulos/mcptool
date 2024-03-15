from typing import Union

from .get_server import JavaServerData, BedrockServerData


class ShowMinecraftServer:
    def __init__(self) -> None:
        pass

    @staticmethod
    def show(self, server_data: Union[JavaServerData, BedrockServerData]) -> None:
        """
        Method to show the server data
        """

        print(f'Platform: {server_data.platform}')
        print(f'IP Address: {server_data.ip_address}')
        print(f'Port: {server_data.port}')
        print(f'MOTD: {server_data.motd}')
        print(f'Version: {server_data.version}')
        print(f'Protocol: {server_data.protocol}')
        print(f'Connected Players: {server_data.connected_players}')
        print(f'Max Players: {server_data.max_players}')

        if isinstance(server_data, JavaServerData):
            print(f'Players: {server_data.players}')
            print(f'Mod: {server_data.mod}')
            print(f'Mods: {server_data.mods}')
            print(f'Favicon: {server_data.favicon}')
            print(f'Ping: {server_data.ping}')
            print(f'Bot Output: {server_data.bot_output}')