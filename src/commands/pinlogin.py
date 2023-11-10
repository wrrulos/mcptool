import subprocess
import os

from src.decoration.paint import paint
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities 
from src.utilities.check_utilities import CheckUtilities


def pinlogin_command(server, username, version, password_file, *args):
    """
    Connect a bot to the specified server to try to guess the user's pin.

    Args:
        server (str): The IP address or domain of the server.
        username (str): The Minecraft username to use for the connection.
        version (str): The Minecraft version to use for the connection.
        password_file (str): The path to the file containing a list of PINs.
        *args: Additional arguments (not used in this function).
    """

    try:
        if not os.path.exists(password_file):
            # Display an error message if the password file does not exist
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", password_file)}')
            return
        
        # Get information about the specified Minecraft server.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "gettingDataFromServer"])}')
        server_data = GetMinecraftServerData.get_data(server, bot=False)

        if server_data is None:
            # Display an error message if server information cannot be retrieved.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')
            return

        # Extract the server IP address and port from the server data.
        server = server_data['ip_port']
        ip, port = server.split(':')

        with open(password_file, 'r', encoding=CheckUtilities.check_file_encoding(password_file)) as f:
            passwords = f.readlines()

        if len(passwords) == 0:
            # Display an error message if the password file is empty
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "pinlogin", "emptyFile"])}')
            return

        if JsonManager.get(["minecraftServerOptions", "proxy"]):
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./mcptool_files/scripts/pinlogin.js {ip} {port} {username} {version} {password_file} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

        else:
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./mcptool_files/scripts/pinlogin.js {ip} {port} {username} {version} {password_file} {len(GetUtilities.get_spaces())}'
        
        # Run the connection script to connect to the server with PIN-based login.
        subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        # Handle keyboard interruption gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
