from loguru import logger
from mccolors import mcwrite

from ..utilities.minecraft.nbt.server_dat import ServersDAT
from ..utilities.managers.language_utils import LanguageUtils as LM


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'clearservers'

    @logger.catch
    def execute(self, arguments: list = []) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        mcwrite(LM.get(f'commands.{self.name}.serversCleared'))
        ServersDAT().remove_servers_dat_file()