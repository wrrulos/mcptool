import os
import requests
import shutil

from utils.checks.Folder import check_folders
from utils.color.TextColor import paint
from utils.gets.Language import language


def update_velocity(url):
    """ 
    Update Velocity.jar and replace the current one 

    Parameters:
    url (str): Velocity download link
    """

    temp_folder = 'mcptool_temp'
    check_folders(temp_folder)

    with open(f'{temp_folder}/Velocity.jar', 'wb') as f:
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["DOWNLOADING_UPDATE"]}')
        velocity = requests.get(url)
        f.write(velocity.content)

    os.remove('utils/velocity/fakeproxy/Velocity.jar')
    os.remove('utils/velocity/velocity/Velocity.jar')
    shutil.copy('mcptool_temp/Velocity.jar', 'utils/velocity/fakeproxy/Velocity.jar')
    shutil.copy('mcptool_temp/Velocity.jar', 'utils/velocity/velocity/Velocity.jar')
    os.remove('mcptool_temp/Velocity.jar')
    os.rmdir('mcptool_temp')
    paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["UPDATE_COMPLETED"].replace("[0]", "Velocity")}')