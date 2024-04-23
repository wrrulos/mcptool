from typing import Union
from mccolors import mcwrite
from loguru import logger

from ..utilities.minecraft.server.get_server import MCServerData, JavaServerData, BedrockServerData
from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.path.mcptool_path import MCPToolPath


class StartProxy:
    def __init__(self, target: str, proxy: str, velocity_forwarding_mode: Union[str, None]) -> None:
        self.target: str = target
        self.proxy: str = proxy
        self.velocity_forwarding_mode: Union[str, None] = velocity_forwarding_mode
        self.proxy_path: str = ''

    @logger.catch
    def run(self):
        """
        Method to start the proxy
        """

        # Get the server data
        server_data: Union[JavaServerData, BedrockServerData, None] = MCServerData(target=self.target, bot=False).get()
        
        if server_data is None:
            mcwrite(LM().get(['errors', 'serverOffline']))
            return
        
        if server_data.platform != 'Java':
            mcwrite(LM().get(['errors', 'notJavaServer']))
            return
        
        self._configure_proxy()

    @logger.catch
    def _configure_proxy(self) -> None:
        """
        Method to configure the proxy
        """

        mcptool_path: str = MCPToolPath().get()
        self.proxy_path: str = f'{mcptool_path}/proxies/{self.proxy}'
        
        # Check if the proxy exists
        if not MCPToolPath().check_file(self.proxy_path):
            mcwrite(LM().get(['errors', 'proxyPathNotFound']))
            logger.error(f'Proxy path not found: {self.proxy_path}')
            return
