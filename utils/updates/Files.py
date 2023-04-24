import time

from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.managers.Updater import Updater
from utils.minecraft.UpdateVersions import update_versions


def update_files():
    """ Check for updates and if necessary, update it. """

    u = Updater()

    paint(f'\n    {language["script"]["PREFIX"]}{language["version_file_messages"]["UPDATE_CHECK"].replace("[0]", "WaterFall")}')

    try:
        if u.check_files_update():
            paint(f'\n    {language["script"]["PREFIX"]}{language["version_file_messages"]["UPDATE_AVAILABLE"]}')
            update_versions()
        
        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["version_file_messages"]["NO_UPDATES_FOUND"]}')

    except KeyError:
        paint(f'\n    {language["script"]["PREFIX"]}{language["version_file_messages"]["UPDATE_FAILED"]}')
        time.sleep(1)

    except KeyboardInterrupt:
        return