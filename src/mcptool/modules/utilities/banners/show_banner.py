import subprocess

from mccolors import mcwrite
from loguru import logger


class ShowBanner:
    def __init__(self, banner: str, clear_screen: bool = False):
        self.banner: str = banner
        self.clear_screen: bool = clear_screen

    @logger.catch
    def show(self) -> None:
        """
        Method to show the banner
        """
        
        # Clear the screen
        if self.clear_screen:
            subprocess.run('clear || cls ', shell=True)
                
        # Print the banner
        mcwrite(self.banner)
