from typing import Union
from easyjsonpy import get_config_value
from loguru import logger
from mccolors import mcwrite

from . import JavaServerData, BedrockServerData
from .get_server_mcstatus_lib import MCServerData
from .get_server_mcstatus_api import MCStatusIOAPI
from ....utilities.managers.language_utils import LanguageUtils as LM


class ServerData:
    def __init__(self, target: str, bot: bool = True) -> None:
        self.target = target
        self.bot = bot

    @logger.catch
    def get_data(self) -> Union[JavaServerData, BedrockServerData, None]:
        """
        Method to get the server data from the server class.

        Returns:
            Union[JavaServerData, BedrockServerData, None]: The server data if the server is online, otherwise None
        """

        if get_config_value('serverDataApi') == 'serverDataApi' or get_config_value('serverDataApi') not in ['local', 'mcstatus.io']:  # :TODO: Replace with None after testing
            logger.error('The serverDataApi is not set in the configuration file')
            mcwrite(LM.get('errors.serverDataApiNotSet'))
            return None

        if get_config_value('serverDataApi') == 'local':
            data: Union[JavaServerData, BedrockServerData, None] = MCServerData(target=self.target, bot=self.bot).get()

        if get_config_value('serverDataApi') == 'mcstatus.io':
            data: Union[JavaServerData, BedrockServerData, None] = MCStatusIOAPI(target=self.target, bot=self.bot).get()

        return data
