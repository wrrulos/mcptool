#!/usr/bin/python3

# This script is in charge of looking for MCPTool updates 
# and if it is necessary to update it using the functions 
# of the Updater() class.

import subprocess
import shutil
import time
import sys
import os

from utils.managers.Settings import SettingsManager
from utils.banners.PrintBanner import print_banner
from utils.gets.Language import language
from utils.managers.Updater import Updater

sm = SettingsManager()
settings = sm.read('settings')
u = Updater()


def update_mcptool():
    """
    Check for updates and if necessary, update it.
    """

    checking_updates = language['banners']['update']['CHECKING_UPDATES']
    new_version = language['banners']['update']['NEW_VERSION']
    downloading = language['banners']['update']['DOWNLOADING']
    extracting = language['banners']['update']['EXTRACTING']
    not_found = language['banners']['update']['NOT_FOUND']
    finished = language['banners']['update']['FINISHED']
    title = language['banners']['update']['TITLE']
    error = language['banners']['update']['ERROR']
    new_script = False

    try:
        print_banner('update', title, checking_updates, '', '', '', '')
        time.sleep(1)
        update = u.check_mcptool_updates()

        if update:
            print_banner('update', title, checking_updates, new_version, '', '', '')
            time.sleep(1)
            print_banner('update', title, checking_updates, new_version, downloading, '', '')
            time.sleep(1)

            if u.download('MCPTool.zip', 'https://github.com/wrrulos/MCPTool/releases/latest/download/MCPTool.zip', '../New-MCPTool'):
                print_banner('update', title, checking_updates, new_version, downloading, extracting, '')
                time.sleep(1)

                if u.extracting('../New-MCPTool/MCPTool.zip', '../New-MCPTool/'):
                    print_banner('update', title, checking_updates, new_version, downloading, extracting, finished)
                    time.sleep(1)
                    folders = os.listdir('../New-MCPTool')
                    folder = folders[0]

                    if os.path.exists('ngrok'):
                        shutil.copy('ngrok', f'../New-MCPTool/{folder}/ngrok')

                    if os.path.exists('ngrok.exe'):
                        shutil.copy('ngrok.exe', f'../New-MCPTool/{folder}/ngrok.exe')
                    
                    new_script = True
                    subprocess.run(f'cd ../New-MCPTool/{folder}/ && {settings["PYTHON_COMMAND"]} main.py', shell=True)
                    sys.exit()

                print_banner('update', title, checking_updates, new_version, downloading, extracting, error)
                time.sleep(3)
                return

            print_banner('update', title, checking_updates, new_version, downloading, error, '')
            time.sleep(3)
            return

        print_banner('update', title, checking_updates, not_found, '', '', '')
        time.sleep(3)
        return

    except KeyboardInterrupt:
        if new_script:
            sys.exit()

        return