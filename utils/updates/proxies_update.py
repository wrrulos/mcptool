import time

from utils.color.text_color import paint
from utils.checks.check_termux import check_termux
from utils.banners.print_banner import print_banner
from utils.managers.language_manager import language_manager
from utils.managers.updater_manager import Updater
from utils.velocity.update_velocity import update_velocity
from utils.waterfall.update_waterfall import update_waterfall
from utils.gets.get_spaces import get_spaces


def update_proxies():
    """ Check for updates and if necessary, update it. """

    u = Updater()
    proxy_update_name = 'proxy_update' if not check_termux() else 'proxy_update_termux'
    print_banner(proxy_update_name)
    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["updateCheck"].replace("[0]", "WaterFall")}')

    try:
        url = u.check_waterfall_update()

        if url is not None:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["updateAvailable"].replace("[0]", "WaterFall")}')
            update_waterfall(url)
        
        else:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["noUpdatesFound"]}')

        time.sleep(1)
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["updateCheck"].replace("[0]", "Velocity")}')
        url = u.check_velocity_update()

        if url is not None:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["updateAvailable"].replace("[0]", "Velocity")}')
            update_velocity(url)

        else:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["noUpdatesFound"]}')

    except KeyError:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["updateFailed"]}')
        time.sleep(1)

    except KeyboardInterrupt:
        return
