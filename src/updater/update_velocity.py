import os
import requests
import shutil

from src.utilities.get_utilities import GetUtilities
from src.decoration.paint import paint


def update_velocity(url):
    """ 
    Update Velocity.jar and replace the current one 

    Args:
        url (str): Velocity download link
    """

    temp_folder = 'mcptool_temp'
    os.makedirs(temp_folder, exist_ok=True)

    with open(f'{temp_folder}/Velocity.jar', 'wb') as f:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "downloadingUpdate"])}')
        velocity = requests.get(url)
        f.write(velocity.content)

    os.remove('mcptool_files/proxy/jar/fakeproxy/Velocity.jar')
    os.remove('mcptool_files/proxy/jar/velocity/Velocity.jar')
    shutil.copy('mcptool_temp/Velocity.jar', 'mcptool_files/proxy/jar/fakeproxy/Velocity.jar')
    shutil.copy('mcptool_temp/Velocity.jar', 'mcptool_files/proxy/jar/velocity/Velocity.jar')
    os.remove('mcptool_temp/Velocity.jar')
    shutil.rmtree('mcptool_temp')
    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "updateCompleted"]).replace("[0]", "Velocity")}')
