import time

from src.managers.log_manager import LogManager
from src.managers.json_manager import JsonManager
from src.decoration.paint import paint
from src.utilities.get_utilities import GetUtilities
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData


def listening_command(server, *args):
    """
    Listen to players who enter the Minecraft server and save their names and UUIDs.

    Args:
        server (str): IP Address and Port of the Minecraft server.
        *args: Additional arguments (not used in this function).

    This function continuously monitors the Minecraft server for incoming players.
    When players join, it captures and displays their usernames and UUIDs on the screen.
    Players are tracked in real-time while the function is running, and it can be interrupted with Ctrl+C.
    """

    captured_players = []  # List to store captured player information
    found = False  # Flag to check if players have been found
    t = ''  # Temporary string for formatting output

    try:
        # Check if the provided server is valid
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

        # Display a message indicating that the function is waiting for players
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "listening", "waitingForPlayers"])}\n')
        
        if JsonManager.get('logs'):
            log_file = LogManager.create_log_file('listening')
            LogManager.write_log(log_file, 'listening', f'Target: {server}\n')

    except KeyboardInterrupt:
        # Handle a Ctrl+C interruption gracefully
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
        return

    while True:
        try:
            # Retrieve data about the Minecraft server
            server_data = GetMinecraftServerData.get_data(server, bot=False)

            if server_data is not None:
                # Check if the server is running Java Edition (not Bedrock)
                if server_data['platform_type'] == 'Bedrock':
                    continue

                # Check if the server has a default player list
                if server_data['default_player_list'] is not None:
                    for player in server_data['default_player_list']:
                        if type(player) is dict:
                            username = player['name']
                            uuid = player.get('uuid', player.get('id', None))

                            # Skip players without a UUID
                            if uuid is None:
                                continue

                            # Check if players have been found
                            if not found:
                                # Display a message when players are found
                                paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "listening", "foundPlayers"])}\n')
                                t = '\n'
                                found = True

                            # Check if this player has already been captured
                            if f'{username} ({uuid})' not in captured_players:
                                # Add the player to the captured list and log their data
                                captured_players.append(f'{username} ({uuid})')
                                log_data = f'{username} ({uuid})'

                                if JsonManager.get('logs'):
                                    LogManager.write_log(log_file, 'listening', log_data)
                                
                                # Display the player's username and UUID
                                paint(f'{GetUtilities.get_spaces()}&f&l{username} ({GetUtilities.get_uuid_color(username, uuid)}{uuid}&f&l)')

            else:
                # If no server data is available, wait for 30 seconds before checking again
                time.sleep(30)

            # Sleep for 1 second before checking again
            time.sleep(1)

        except KeyboardInterrupt:
            # Handle a Ctrl+C interruption gracefully and exit the loop
            paint(f'{t}{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
            break
