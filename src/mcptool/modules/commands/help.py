import subprocess

from loguru import logger
from mccolors import mcwrite

from ...modules.utilities.banners.banners import HelpBanners
from ...modules.utilities.banners.show_banner import ShowBanner


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'help'

    @logger.catch
    def execute(self, arguments: list = []) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        ShowBanner(HelpBanners.HELP_BANNER_1).show()
