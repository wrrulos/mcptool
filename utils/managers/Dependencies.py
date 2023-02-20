#!/usr/bin/python3

import subprocess
import time
import os

from utils.gets.Language import language
from utils.managers.Settings import SettingsManager
from utils.banners.PrintBanner import print_banner

dependencies = {
    'Java': "java -version # https://www.java.com/es/",
    'Nmap': 'nmap --version # https://nmap.org/download.html',
    'NodeJS': 'npm --version # https://nodejs.org/es/'
}

sm = SettingsManager()
settings = sm.read('settings')


class Dependencies:
    def __init__(self) -> None:
        pass

    def check_dependencies(self):
        """ Check if dependencies are installed """

        msg1 = language['banners']['dependencies']['MESSAGE1']
        msg2 = language['banners']['dependencies']['MESSAGE2']
        msg3 = language['banners']['dependencies']['MESSAGE3']
        msg4 = language['banners']['dependencies']['MESSAGE4']

        for dependence in dependencies.items():
            i = dependence[1].split(' # ')
            if subprocess.call(f'{i[0]} >nul 2>&1', shell=True) != 0:
                print_banner(f'dependencies{settings["TYPE_OF_BANNERS"]}', msg1, msg2, msg3, dependence[0], msg4, i[1])
                time.sleep(3)
                return False

        if not os.path.isfile('ngrok.exe') and not os.path.isfile('ngrok'):
            print_banner(f'dependencies{settings["TYPE_OF_BANNERS"]}', msg1, msg2, msg3, 'Ngrok', msg4, 'https://dashboard.ngrok.com/get-started/setup')
            time.sleep(3)
            return False

        self.python_variable()
        return True

    def python_variable(self):
        """ 
        First check if the python variable configuration 
        does not contain the values ​shown below.

        Why do this? This is in case the user has saved a 
        variable other than 'normal', such as 'py' and 
        this way mcptool doesn't overwrite it.

        Then Store the python variable in the config
        depending on the operating system.
        """

        values = ['', 'python', 'python3']

        if settings['PYTHON_COMMAND'] in values:
            if os.name == 'nt':
                sm.write('settings', 'PYTHON_COMMAND', 'python')

            else:
                sm.write('settings', 'PYTHON_COMMAND', 'python3')



