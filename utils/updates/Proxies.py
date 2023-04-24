import time

from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.managers.Updater import Updater
from utils.velocity.UpdateVelocity import update_velocity
from utils.waterfall.UpdateWaterFall import update_waterfall


def update_proxies():
    """ Check for updates and if necessary, update it. """

    u = Updater()

    paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["UPDATE_CHECK"].replace("[0]", "WaterFall")}')

    try:
        url = u.check_waterfall_update()

        if url is not None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["UPDATE_AVAILABLE"].replace("[0]", "WaterFall")}')
            update_waterfall(url)
        
        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["NO_UPDATES_FOUND"]}')

        time.sleep(1)
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["UPDATE_CHECK"].replace("[0]", "Velocity")}')

        url = u.check_velocity_update()

        if url is not None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["UPDATE_AVAILABLE"].replace("[0]", "Velocity")}')
            update_velocity(url)

        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["NO_UPDATES_FOUND"]}')

    except KeyError:
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["UPDATE_FAILED"]}')
        time.sleep(1)

    except KeyboardInterrupt:
        return