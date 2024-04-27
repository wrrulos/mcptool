import subprocess
import time
import os

from typing import Union
from mccolors import mcwrite
from loguru import logger

from ....utilities.minecraft.server.get_server import MCServerData, JavaServerData, BedrockServerData
from ....utilities.managers.language_manager import LanguageManager as LM
from ...path.mcptool_path import MCPToolPath
from ...constants import OS_NAME
from .jar import JarManager


class StartProxy:
    def __init__(self, target: str, proxy: str, velocity_forwarding_mode: Union[str, None]) -> None:
        self.target: str = target
        self.proxy: str = proxy
        self.velocity_forwarding_mode: Union[str, None] = velocity_forwarding_mode
        self.proxy_path: str = ''
        self.proxy_settings: str = ''
        self.proxy_settings_path: str = ''

    @logger.catch
    def setup(self):
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

        # If the proxy settings are empty, return because the proxy could not be configured
        if self.proxy_settings == '':
            return
        
        process: subprocess.Popen = self._start_proxy()
        stdout, stderr = process.communicate()
        
        time.sleep(2)
        
        if process.poll() is not None:
            stderr = stderr.decode('utf-8')

            if 'this version of the Java Runtime':
                mcwrite(LM().get(['errors', 'javaVersionNotSupported']))
                logger.error(f'Java version error: {stderr}')
                return
            
            mcwrite(LM().get(['errors', 'proxyNotStartedUnkownError']))
            logger.error(f'Proxy not started: {self.proxy}. Reason: {stderr}')
            return

    @logger.catch
    def _configure_proxy(self) -> None:
        """
        Method to configure the proxy
        """

        mcwrite(LM().get(['commands', 'proxy', 'configuringProxy']).replace('%proxyType%', self.proxy))
        time.sleep(0.5)

        mcptool_path: str = MCPToolPath().get()
        self.proxy_path: str = f'{mcptool_path}/proxies/{self.proxy}'
        
        # Check if the proxy exists
        if not os.path.exists(self.proxy_path):
            mcwrite(LM().get(['errors', 'proxyPathNotFound']))
            logger.error(f'Proxy path not found: {self.proxy_path}')
            return

        if self.proxy == 'waterfall':
            self.proxy_settings_path = f'{mcptool_path}/txt/waterfall.config'
            config_file: str = f'{self.proxy_path}/config.yml'

        if self.proxy == 'velocity':
            self.proxy_settings_path = f'{mcptool_path}/txt/velocity.config'
            config_file: str = f'{self.proxy_path}/velocity.toml'

        try:  # Check if the proxy settings exist
            with open(self.proxy_settings_path, 'r') as file:
                self.proxy_settings = file.read()

        except FileNotFoundError:
            mcwrite(LM().get(['errors', 'proxySettingsNotFound']))
            logger.error(f'Proxy settings not found: {self.proxy_settings_path}')
            return
        
        # Replace the placeholders with the target, port and forwarding mode
        self.proxy_settings = self.proxy_settings.replace('[[ADDRESS]]', self.target)
        self.proxy_settings = self.proxy_settings.replace('[[PORT]]', '25567')

        # In case of velocity, replace the forwarding mode
        self.proxy_settings = self.proxy_settings.replace('[[MODE]]', self.velocity_forwarding_mode[0])

        # Clear the config file and write the new settings
        with open(config_file, 'w+') as file:
            file.truncate(0)
            file.write(self.proxy_settings)

    @logger.catch
    @staticmethod
    def _start_proxy(self) -> subprocess.Popen:
        """
        Method to start the proxy
        """

        # Check if the proxy exists. If not, download it
        JarManager(jar_name=self.proxy, jar_path=self.proxy_path).check()

        if not os.path.exists(f'{self.proxy_path}/{self.proxy}.jar'):
            mcwrite(LM().get(['errors', 'proxyJarNotFound']))
            logger.critical(f'Proxy jar not found: {self.proxy_path}/{self.proxy}.jar')
            return
        
        # Start the proxy
        command: str = f'cd {self.proxy_path} && java -jar {self.proxy}.jar'

        if OS_NAME == 'windows':
            command = f'C: && {command}'

        process: subprocess.Popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process