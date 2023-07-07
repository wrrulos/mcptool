import os
import requests
import shutil

from utils.checks.check_folder import check_folders
from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_spaces import get_spaces


def update_waterfall(url):
    """ 
    Update waterfall.jar and replace the current one 

    Args:
        url (str): Waterfall download link
    """

    temp_folder = 'mcptool_temp'
    check_folders(temp_folder)

    with open(f'{temp_folder}/WaterFall.jar', 'wb') as f:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["downloadingUpdate"]}')
        waterfall = requests.get(url)
        f.write(waterfall.content)

    os.remove('utils/waterfall/proxy/WaterFall.jar')
    shutil.copy('mcptool_temp/WaterFall.jar', 'utils/waterfall/proxy/WaterFall.jar')
    os.remove('mcptool_temp/WaterFall.jar')
    os.rmdir('mcptool_temp')
    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["updateCompleted"].replace("[0]", "WaterFall")}')
