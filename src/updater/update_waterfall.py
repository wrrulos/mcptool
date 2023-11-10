import os
import requests
import shutil

from src.utilities.get_utilities import GetUtilities
from src.decoration.paint import paint


def update_waterfall(url):
    """ 
    Update waterfall.jar and replace the current one 

    Args:
        url (str): waterfall download link
    """

    temp_folder = 'mcptool_temp'
    os.makedirs(temp_folder, exist_ok=True)

    with open(f'{temp_folder}/waterfall.jar', 'wb') as f:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "downloadingUpdate"])}')
        waterfall = requests.get(url)
        f.write(waterfall.content)

    os.remove('mcptool_files/proxy/jar/waterfall/waterfall.jar')
    shutil.copy('mcptool_temp/waterfall.jar', 'mcptool_files/proxy/jar/waterfall/waterfall.jar')
    os.remove('mcptool_temp/waterfall.jar')
    shutil.rmtree('mcptool_temp')
    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "updateCompleted"]).replace("[0]", "waterfall")}')
