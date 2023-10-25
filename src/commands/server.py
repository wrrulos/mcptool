from src.decoration.paint import paint
from src.minecraft.show_minecraft_server import show_server
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData
from src.utilities.get_utilities import GetUtilities
from src.managers.log_manager import LogManager


def server_command(server, *args):
    """
    Retrieve information about the specified Minecraft server and display it on the screen.

    Args:
        server (str): The IP address or domain of the Minecraft server.
        *args: Additional arguments (not used in this function).
    """

    try:
        # Retrieve server data using the specified server IP/domain.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "gettingDataFromServer"])}')
        server_data = GetMinecraftServerData.get_data(server)

        # Check if the server_data is valid
        if server_data is not None:
            # Display the server information on the screen.
            show_server(server_data)

            # Create a log file for server-related information.
            log_file = LogManager.create_log_file('server')

            # Prepare the server data for logging and write it to the log file.
            log_data = list(server_data.values())
            LogManager.write_log(log_file, 'server', log_data)

        else:
            # Handle the case when server_data is None or invalid.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')

    except (KeyboardInterrupt):
        # Handle a KeyboardInterrupt (Ctrl+C) gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

