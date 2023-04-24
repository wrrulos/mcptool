from utils.banners.PrintBanner import print_banner
from utils.managers.Settings import SettingsManager


def help_command(*args):
    """ 
    Shows the list of corresponding commands.
    """

    sm = SettingsManager()
    settings = sm.read('settings')
    print_banner(f'help{settings["TYPE_OF_BANNERS"]}')