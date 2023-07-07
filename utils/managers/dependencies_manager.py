import subprocess
import time

from utils.banners.banner_messages import *
from utils.banners.print_banner import print_banner
from utils.checks.check_termux import check_termux
from utils.managers.config_manager import config_manager

dependencies = {
    'Java': "java -version # https://www.java.com/es/",
    'NodeJS': 'npm --version # https://nodejs.org/es/'
}


class Dependencies:
    def __init__(self) -> None:
        pass

    def check_dependencies(self):
        """ Check if dependencies are installed """

        dependencies_banner_name = f'dependencies{config_manager.config["typeOfBanners"]}' if not check_termux() else 'dependencies_termux'

        try:
            for dependence in dependencies.items():
                i = dependence[1].split(' # ')
                if subprocess.call(f'{i[0]} >nul 2>&1', shell=True) != 0:
                    print_banner(dependencies_banner_name, dependencies_message1, dependencies_message2, dependencies_message3, dependence[0], dependencies_message4, i[1])
                    time.sleep(3)
                    return False
                
        except KeyboardInterrupt:
            pass
        
        return True
