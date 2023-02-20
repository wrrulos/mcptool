#!/usr/bin/python3

from utils.managers.Settings import SettingsManager
from utils.banners.PrintBanner import print_banner

sm = SettingsManager()
settings = sm.read('settings')


def help_command():
    """ 
    Command that displays command help
    """

    print_banner(f'help{settings["TYPE_OF_BANNERS"]}')