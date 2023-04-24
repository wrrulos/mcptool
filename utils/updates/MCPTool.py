import os
import shutil
import subprocess
import sys
import time

from utils.banners.BannerMessages import *
from utils.banners.PrintBanner import print_banner
from utils.managers.Settings import SettingsManager
from utils.managers.Updater import Updater


def update_mcptool():
    """ Check for updates and if necessary, update it. """

    sm = SettingsManager()
    settings = sm.read('settings')
    u = Updater()

    new_script = False

    # Messages
    try:
        print_banner('update', update_title, update_checking_updates, '', '', '', '')
        time.sleep(1)
        update = u.check_mcptool_updates()

        if update:
            print_banner('update', update_title, update_checking_updates, update_new_version, '', '', '')
            time.sleep(1)
            print_banner('update', update_title, update_checking_updates, update_new_version, update_downloading, '', '')
            time.sleep(1)

            if u.download('MCPTool.zip', 'https://github.com/wrrulos/MCPTool/releases/latest/download/MCPTool.zip', '../New-MCPTool'):
                print_banner('update', update_title, update_checking_updates, update_new_version, update_downloading, update_extracting, '')
                time.sleep(1)

                if u.extracting('../New-MCPTool/MCPTool.zip', '../New-MCPTool/'):
                    print_banner('update', update_title, update_checking_updates, update_new_version, update_downloading, update_extracting, update_finished)
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

                print_banner('update', update_title, update_checking_updates, update_new_version, update_downloading, update_extracting, update_error)
                time.sleep(2.5)
                return

            print_banner('update', update_title, update_checking_updates, update_new_version, update_downloading, update_error, '')
            time.sleep(2.5)
            return

        print_banner('update', update_title, update_checking_updates, update_not_found, '', '', '')
        time.sleep(2.5)
        return

    except KeyboardInterrupt:
        if new_script:
            sys.exit()

        return