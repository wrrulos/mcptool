import subprocess

from src.managers.json_manager import JsonManager
from src.decoration.print_banner import print_banner
from src.utilities.check_utilities import CheckUtilities
from src.utilities.get_utilities import GetUtilities


def clear_command(*args):
    """
    Clear the terminal screen and display a new banner.

    Args:
        *args: Additional arguments (not used in this function).
    """

    # Get configuration settings from JSON.
    version = JsonManager.get('currentVersion')
    discord_presence = '✔️' if JsonManager.get('discordPresence') else '❌'
    bot = '✔️' if JsonManager.get(['minecraftServerOptions', 'checkServerLoginWithABot']) else '❌'
    proxy = '✔️' if JsonManager.get(['minecraftServerOptions', 'proxy']) else '❌'

    # Clear the terminal screen, supporting both Unix-like and Windows systems.
    subprocess.run('clear || cls', shell=True)

    # Display a new banner based on configuration settings.
    if CheckUtilities.check_termux():
        # Display the Termux-compatible menu banner.
        print_banner('menu_termux', GetUtilities.get_translated_text(['banners', 'menu_termux', 'message1']), GetUtilities.get_translated_text('credits'), version, GetUtilities.get_translated_text(['banners', 'menu_termux', 'message3']))
        
    else:
        print_banner('menu', GetUtilities.get_translated_text(['banners', 'menu', 'message1']), GetUtilities.get_translated_text(['banners', 'menu', 'message2']), version, discord_presence, bot, proxy)
