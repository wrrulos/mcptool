import os
import re

from src.decoration.paint import paint
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities
from src.minecraft.show_minecraft_server import show_server
from src.managers.log_manager import LogManager


def checker_command(file, *args):
    """
    Check Minecraft servers listed in a file and display their information.

    Args:
        file (str): The path to the file containing a list of Minecraft servers to check.
        *args: Additional arguments (not used in this function).
    """
    
    try:
        servers_found = 0
        log_file = LogManager.create_log_file('checker')

        # Check if the specified file exists
        if not os.path.exists(file):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", file)}')
            return
        
        # Display a message indicating that servers are being checked in the file
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "checker", "checking"])}')

        # Open the file and look for servers in each line
        with open(file, encoding=CheckUtilities.check_file_encoding(file)) as f:
            for line in f:
                # Use regular expression to find server addresses in the line
                servers = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)

                for server in servers:
                    # Get data for each server
                    server_data = GetMinecraftServerData.get_data(server)
                            
                    if server_data is not None:                            
                        show_server(server_data)
                        servers_found += 1

                        if JsonManager.get('logs'):
                            log_data = list(server_data.values())
                            LogManager.write_log(log_file, 'scan', log_data)

        if servers_found == 0:
            # No servers were found in the file
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "checker", "noServersInTheFile"])}')

        else:
            # Servers were found and displayed
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "checker", "foundServers"]).replace("[0]", str(servers_found))}')

    except KeyboardInterrupt:
        # Handle keyboard interruption gracefully
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
