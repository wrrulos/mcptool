from loguru import logger

from ...modules.utilities.banners.banners import DiscordBanners
from ...modules.utilities.banners.show_banner import ShowBanner


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'discord'

    @logger.catch
    def execute(self, arguments: list = []) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        ShowBanner(DiscordBanners.DISCORD_BANNER_1).show()
