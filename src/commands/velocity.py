from src.decoration.paint import paint
from src.utilities.get_utilities import GetUtilities
from src.proxy.launcher import ProxyLauncher


def velocity_command(target, mode, *args):
    """
    Start a Velocity proxy to perform actions on a target server.

    Args:
        target (str): The target server's IP address or domain.
        mode (str): The mode to use for the Velocity proxy.
        *args: Additional arguments (not used in this function).
    """
    
    try:
        # Check if the specified forwarding mode is valid
        if mode.lower() not in ['none', 'legacy', 'bungeeguard', 'modern']:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidForwardingMode"])}')
            return
        
        # Start the Velocity proxy with the specified target and mode
        ProxyLauncher.start_proxy('velocity', target, mode)

    except KeyboardInterrupt:
        # Handle keyboard interruption gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
