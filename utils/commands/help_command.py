from utils.banners.print_banner import print_banner
from utils.checks.check_termux import check_termux
from utils.managers.config_manager import config_manager


def help_command(*args):
    """ 
    Shows the list of corresponding commands.
    """

    if check_termux():
        print_banner('help_termux')

    else:
        print_banner(f'help{config_manager.config["typeOfBanners"]}')
