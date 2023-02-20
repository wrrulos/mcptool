#!/usr/bin/python3

import requests
import shutil
import os

from utils.checks.Folder import check_folders
from utils.gets.Language import language
from utils.color.TextColor import paint


def update_waterfall(url):
    """ 
    Update waterfall.jar and replace the current one 

    :param url: Waterfall URL
    """

    temp_folder = 'mcptool_temp'
    check_folders(temp_folder)

    with open(f'{temp_folder}/WaterFall.jar', 'wb') as f:
        paint(f'\n    {language["script"]["PREFIX"]}{language["waterfall_messages"]["DOWNLOADING_UPDATE"]}')
        waterfall = requests.get(url)
        f.write(waterfall.content)

    os.remove('utils/waterfall/proxy/poisoning/WaterFall.jar')
    os.remove('utils/waterfall/proxy/bungee/WaterFall.jar')
    shutil.copy('mcptool_temp/WaterFall.jar', 'utils/waterfall/proxy/poisoning/WaterFall.jar')
    shutil.copy('mcptool_temp/WaterFall.jar', 'utils/waterfall/proxy/bungee/WaterFall.jar')
    os.remove('mcptool_temp/WaterFall.jar')
    os.rmdir('mcptool_temp')
    