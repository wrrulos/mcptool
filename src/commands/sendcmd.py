import subprocess
import time
import os

from src.decoration.paint import paint
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities 
from src.utilities.check_utilities import CheckUtilities


def sendcmd_command(server, username, version, command_file, loop, *args):
    """
    Connects to the specified Minecraft server and executes a series of commands from a file.

    Args:
        server (str): The IP address or domain of the Minecraft server.
        username (str): The Minecraft username to use for the connection.
        version (str): The Minecraft version to use for the connection.
        command_file (str): The path to a file containing a list of commands to execute.
        loop (bool): A flag to indicate whether the commands should be executed in a loop.
        *args: Additional arguments (not used in this function).
    """

    try:
        # Check if the provided command file exists
        if not os.path.exists(command_file):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", command_file)}')
            return
        
        if not CheckUtilities.check_loop_argument(loop):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidLoopArgument"])}')
            return
        
        loop = GetUtilities.get_loop_argument(loop)
        
        # Get information about the specified Minecraft server.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "gettingDataFromServer"])}')
        server_data = GetMinecraftServerData.get_data(server, bot=False)

        if server_data is None:
            # Display an error message if the server information cannot be retrieved
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')
            return
        
        if server_data['platform_type'] != 'Java':
            # Display an error message if the server is Bedrock.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "errorBedrockServer"])}')
            return

        # Extract the server IP address and port from the server data.
        server = server_data['ip_port']
        ip, port = server.split(':')

        with open(command_file, 'r', encoding=CheckUtilities.check_file_encoding(command_file)) as f:
            commands = f.readlines()

        if len(commands) == 0:
            # Display a message if the command file is empty
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "sendcmd", "emptyFile"])}')
            return
        
        # Display a message indicating that the command execution is starting
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "sendcmd", "startingTheAttack"])}')
        
        if JsonManager.get(["minecraftServerOptions", "proxy"]):
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./mcptool_files/scripts/sendcmd.js {ip} {port} {username} {version} {command_file} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

        else:
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./mcptool_files/scripts/sendcmd.js {ip} {port} {username} {version} {command_file} {len(GetUtilities.get_spaces())}'
        
        while loop:
            # If 'loop' flag is True, execute the commands in a loop with a 4-second delay between cycles
            time.sleep(4)
            subprocess.run(command, shell=True)

        if not loop:
            # If 'loop' flag is False, execute the commands once
            subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        # Handle keyboard interruption gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
