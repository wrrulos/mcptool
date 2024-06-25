import os
import nbtlib

from nbtlib import File, Compound, String, List


class ServersDAT:
    def __init__(self):
        self.servers_dat_file_path: str = self.get_servers_dat_file_path()

    def add_servers_dat_file(self, servers: list, vulnerables: bool = False) -> None:
        """
        Method to add a server to the servers.dat file.

        Args:
            server (list): The server to add to the servers.dat file
        """

        server_message: str = 'MCPTool Server' if not vulnerables else 'MCPTool - Bungee Exploit Vulnerable'

        if not os.path.exists(self.servers_dat_file_path):
            nbt_file: File = File({'servers': List[Compound]()})
            nbt_file.save(self.servers_dat_file_path)

        nbt_file: File = nbtlib.load(self.servers_dat_file_path)

        # If the servers key does not exist, create it
        servers_dat: List = nbt_file['servers']
        nbt_file['servers'] = List[Compound](servers_dat)
        nbt_file.save(self.servers_dat_file_path)

        # Add the server to the servers.dat file
        nbt_file: File = nbtlib.load(self.servers_dat_file_path)
        servers_dat: List = nbt_file['servers']

        for server in servers:
            servers_dat.append(Compound({'name': String(server_message), 'ip': String(server)}))

        nbt_file['servers'] = servers_dat
        nbt_file.save(self.servers_dat_file_path)

    def get_servers_dat_file_path(self) -> str:
        """
        Method to get the servers.dat file path.

        Returns:
            str: The servers.dat file path
        """

        if os.name == 'nt':  # Windows
            return os.path.join(os.environ['APPDATA'], '.minecraft', 'servers.dat')

        return os.path.join(os.path.expanduser('~'), '.minecraft', 'servers.dat')

    def remove_servers_dat_file(self) -> None:
        """
        Method to remove the servers.dat file.
        """

        if os.path.exists(self.servers_dat_file_path):
            os.remove(self.servers_dat_file_path)
