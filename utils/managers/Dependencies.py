import os
import subprocess
import time

from utils.banners.BannerMessages import *
from utils.banners.PrintBanner import print_banner
from utils.managers.Settings import SettingsManager

dependencies = {
    'Java': "java -version # https://www.java.com/es/",
    'NodeJS': 'npm --version # https://nodejs.org/es/'
}

sm = SettingsManager()
settings = sm.read('settings')


class Dependencies:
    def __init__(self) -> None:
        pass

    def check_dependencies(self):
        """ Check if dependencies are installed """

        try:
            for dependence in dependencies.items():
                i = dependence[1].split(' # ')
                if subprocess.call(f'{i[0]} >nul 2>&1', shell=True) != 0:
                    print_banner(f'dependencies{settings["TYPE_OF_BANNERS"]}', dependencies_message1, dependencies_message2, dependencies_message3, dependence[0], dependencies_message4, i[1])
                    time.sleep(3)
                    return False
                
        except KeyboardInterrupt:
            pass
        
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



