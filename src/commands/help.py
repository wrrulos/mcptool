from src.utilities.check_utilities import CheckUtilities
from src.decoration.print_banner import print_banner
from src.managers.json_manager import JsonManager


def help_command(*args):
    """ 
    Shows the list of corresponding commands.
    """

    if CheckUtilities.check_termux():
        # Display the help banner for Termux
        print_banner('help_termux')
        
    else:
        # Display the help banner based on the configured type of banners
        print_banner(f'help')
