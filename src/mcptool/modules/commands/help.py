import random

from loguru import logger

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

        banner: str = HelpBanners.BANNERS[random.randint(0, len(HelpBanners.BANNERS) - 1)]
        ShowBanner(banner).show()