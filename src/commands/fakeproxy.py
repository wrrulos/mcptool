from src.decoration.paint import paint
from src.proxy.launcher import ProxyLauncher
from src.utilities.get_utilities import GetUtilities


def fakeproxy_command(target, mode, *args):
    """
    Start a FakeProxy proxy server with the specified target server and forwarding mode.

    Args:
        target (str): The IP address and port of the target Minecraft server.
        mode (str): The forwarding mode for FakeProxy ('none', 'legacy', 'bungeeguard', 'modern').
        *args: Additional arguments (not used in this function).
    """

    try:
        # Check if the specified forwarding mode is valid
        if mode.lower() not in ['none', 'legacy', 'bungeeguard', 'modern']:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidForwardingMode"])}')
            return
        
        # Start the FakeProxy proxy server with the specified parameters
        ProxyLauncher.start_proxy('fakeproxy', target, mode)

    except KeyboardInterrupt:
        # Handle keyboard interruption gracefully
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
