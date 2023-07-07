import subprocess

from utils.banners.banner_messages import *
from utils.banners.print_banner import print_banner
from utils.checks.check_termux import check_termux
from utils.managers.config_manager import config_manager


def clear_command():
    """ Clear the terminal screen. """

    mcptool_version = config_manager.config['currentVersion'].split('///')[1]
    banner_name = 'main' if not check_termux() else 'main_termux'

    subprocess.run('clear || cls', shell=True)
    print_banner(banner_name, menu_message1, menu_message2.replace('[0]', mcptool_version), menu_message3, menu_message4, menu_message5, menu_message6, menu_message7)