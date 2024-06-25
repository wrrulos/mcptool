import os
import subprocess

from mccolors import mcwrite
from loguru import logger

from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.path.mcptool_path import MCPToolPath

class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'settings'
        self.arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]


    @logger.catch
    def execute(self, arguments: list) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        if os.name != 'nt':
            mcwrite(LM.get('errors.windowsOnly'))

        settings_path: str = f'{MCPToolPath().get()}/settings.json'
        subprocess.run(['notepad', settings_path])
        mcwrite(LM.get('commands.settings.restartNeeded'))
