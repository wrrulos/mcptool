from src.decoration.paint import paint
from src.utilities.get_utilities import GetUtilities
from src.managers.log_manager import LogManager


def uuid_command(username, *args):
    """ 
    Gets the premium UUID (if possible) and the 
    non-premium UUID of the specified player.
    
    Args:
        username (str): Minecraft username.
        *args: Additional arguments (not used in this function).
    """

    try:
        # Get the premium and non-premium UUIDs for the specified username.
        online_uuid, offline_uuid = GetUtilities.get_player_uuid(username)
        
        # Create a log file to record the results.
        log_file = LogManager.create_log_file('uuid')

        # If the Minecraft user is premium.
        if online_uuid is not None:
            log_data = f'[Username] {username} [UUID Premium] {online_uuid} [UUID No Premium] {offline_uuid}\n'
            
            # Display the premium UUID and non-premium UUID.
            paint(f'\n{GetUtilities.get_spaces()}&4[&cUU&f&lID&4] {GetUtilities.get_translated_text(["commands", "uuid", "onlineUUID"])} {online_uuid}\n{GetUtilities.get_spaces()}&4[&cUU&f&lID&4] {GetUtilities.get_translated_text(["commands", "uuid", "offlineUUID"])} {offline_uuid}')

        else:
            log_data = f'[Username] {username} [UUID No Premium] {offline_uuid}\n'
            
            # Display only the non-premium UUID.
            paint(f'\n{GetUtilities.get_spaces()}&4[&cUU&f&lID&4] {GetUtilities.get_translated_text(["commands", "uuid", "offlineUUID"])} {offline_uuid}')

        # Write the log data to the log file.
        LogManager.write_log(log_file, 'uuid', log_data)

    except KeyboardInterrupt:
        # Handle a KeyboardInterrupt (Ctrl+C) gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
