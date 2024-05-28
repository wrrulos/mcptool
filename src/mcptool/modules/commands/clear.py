import random

from loguru import logger
from mccolors import mcwrite

from ...modules.utilities.banners.banners import MCPToolBanners
from ...modules.utilities.banners.show_banner import ShowBanner


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'clear'

    @logger.catch
    def execute(self, arguments: list = []) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        banner: str = MCPToolBanners.BANNERS[random.randint(0, len(MCPToolBanners.BANNERS) - 1)]
        ShowBanner(banner, clear_screen=True).show()
