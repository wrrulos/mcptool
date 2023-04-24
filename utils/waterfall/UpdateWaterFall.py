import os
import requests
import shutil

from utils.checks.Folder import check_folders
from utils.color.TextColor import paint
from utils.gets.Language import language


def update_waterfall(url):
    """ 
    Update waterfall.jar and replace the current one 

    Parameters:
    url (str): Waterfall download link
    """

    temp_folder = 'mcptool_temp'
    check_folders(temp_folder)

    with open(f'{temp_folder}/WaterFall.jar', 'wb') as f:
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["DOWNLOADING_UPDATE"]}')
        waterfall = requests.get(url)
        f.write(waterfall.content)

    os.remove('utils/waterfall/proxy/WaterFall.jar')
    shutil.copy('mcptool_temp/WaterFall.jar', 'utils/waterfall/proxy/WaterFall.jar')
    os.remove('mcptool_temp/WaterFall.jar')
    os.rmdir('mcptool_temp')
    paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["UPDATE_COMPLETED"].replace("[0]", "WaterFall")}')
