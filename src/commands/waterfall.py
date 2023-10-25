from src.decoration.paint import paint
from src.proxy.launcher import ProxyLauncher
from src.utilities.get_utilities import GetUtilities


def waterfall_command(target, *args):
    """
    Start a Waterfall proxy to connect to a target Minecraft server.

    Args:
        target (str): The IP address or domain of the target Minecraft server.
        *args: Additional arguments (not used in this function).
    """
    
    try:
        # Start the Waterfall proxy with the specified target
        ProxyLauncher.start_proxy('waterfall', target)

    except KeyboardInterrupt:
        # Handle keyboard interruption gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
