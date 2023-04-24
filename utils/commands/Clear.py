import subprocess

from utils.banners.BannerMessages import *
from utils.banners.PrintBanner import print_banner
from utils.managers.Settings import SettingsManager


def clear_command():
    """ Clear the terminal screen. """

    sm = SettingsManager()
    settings = sm.read('settings')
    mcptool_version = settings['CURRENT_VERSION'].split('///')[1]
    
    subprocess.run('cls || clear', shell=True)
    print_banner('main', menu_message1, menu_message2.replace('[0]', mcptool_version), menu_message3, menu_message4, menu_message5, menu_message6, menu_message7)