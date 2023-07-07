import os
import requests
import shutil

from utils.checks.check_folder import check_folders
from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_spaces import get_spaces


def update_velocity(url):
    """ 
    Update Velocity.jar and replace the current one 

    Args:
        url (str): Velocity download link
    """

    temp_folder = 'mcptool_temp'
    check_folders(temp_folder)

    with open(f'{temp_folder}/Velocity.jar', 'wb') as f:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["downloadingUpdate"]}')
        velocity = requests.get(url)
        f.write(velocity.content)

    os.remove('utils/velocity/fakeproxy/Velocity.jar')
    os.remove('utils/velocity/velocity/Velocity.jar')
    shutil.copy('mcptool_temp/Velocity.jar', 'utils/velocity/fakeproxy/Velocity.jar')
    shutil.copy('mcptool_temp/Velocity.jar', 'utils/velocity/velocity/Velocity.jar')
    os.remove('mcptool_temp/Velocity.jar')
    os.rmdir('mcptool_temp')
    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["updateCompleted"].replace("[0]", "Velocity")}')
