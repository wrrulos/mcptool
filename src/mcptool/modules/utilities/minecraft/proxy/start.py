import subprocess
import time
import os

from typing import Union
from mccolors import mcwrite
from loguru import logger

from ....utilities.minecraft.server.get_server import MCServerData, JavaServerData, BedrockServerData
from ....utilities.managers.language_manager import LanguageManager as LM
from ...managers.settings_manager import SettingsManager as SM
from ...path.mcptool_path import MCPToolPath
from ...constants import OS_NAME
from .jar import JarManager


class StartProxy:
    def __init__(self, target: str, proxy: str, velocity_forwarding_mode: Union[str, None]) -> None:
        self.target: str = target
        self.proxy: str = proxy
        self.velocity_forwarding_mode: Union[str, None] = velocity_forwarding_mode
        self.proxy_path: str = ''
        self.proxy_port: int = SM().get(['proxyOptions', f'{self.proxy}Port'])
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
            mcwrite(LM().get(['errors', 'proxyNotConfigured']))
            return
        
        mcwrite(LM().get(['commands', 'proxy', 'proxyConfigured']))
        time.sleep(1)
        mcwrite(LM().get(['commands', 'proxy', 'startingProxy']))
        
        process: subprocess.Popen = self._start_proxy()

        if process is None:
            return
        
        mcwrite(LM().get(['commands', 'proxy', 'proxyStarted']).replace('%proxyIp%', '127.0.0.1').replace('%proxyPort%', str(self.proxy_port)))
        self._read_output(process)
        
    @logger.catch
    def _read_output(self, process: subprocess.Popen) -> None:
        """
        Method to read the output of the proxy
        """

        # Review each line of the process output.
        for line in process.stdout:
            try:
                output_line: str = line.decode('utf-8').strip()

            except UnicodeDecodeError:
                continue

            # If the line contains an error, notify the user and log the error
            if 'this version of the Java Runtime' in output_line:
                mcwrite(LM().get(['errors', 'javaVersionNotSupported']))
                logger.error(f'Java version error: {output_line}')
                return
            
            if 'Invalid or corrupt jarfile' in output_line:
                mcwrite(LM().get(['errors', 'invalidJarFile']))
                logger.error(f'Invalid or corrupt jarfile: {self.proxy}. Reason: {output_line}')
                return
            
            if 'Unable to read/load/save your velocity.toml' in output_line:
                mcwrite(LM().get(['errors', 'velocityTomlError']))
                logger.error(f'Unable to read/load/save your velocity.toml: {output_line}')
                return
            
            #mcwrite(output_line) #! Debugging

        process.wait()

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
            with open(self.proxy_settings_path, 'r', encoding='utf8') as file:
                self.proxy_settings = file.read()

        except FileNotFoundError:
            mcwrite(LM().get(['errors', 'proxySettingsNotFound']))
            logger.error(f'Proxy settings not found: {self.proxy_settings_path}')
            return
        
        # Replace the placeholders with the target, port and forwarding mode
        self.proxy_settings = self.proxy_settings.replace('[[ADDRESS]]', self.target)
        self.proxy_settings = self.proxy_settings.replace('[[PORT]]', str(self.proxy_port))

        # In case of velocity, replace the forwarding mode
        self.proxy_settings = self.proxy_settings.replace('[[MODE]]', self.velocity_forwarding_mode)

        # Clear the config file and write the new settings
        with open(config_file, 'w+', encoding='utf8') as file:
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
            return None
        
        # Start the proxy
        command: str = f'cd {self.proxy_path} && java -jar {self.proxy}.jar'

        if OS_NAME == 'windows':
            command = f'C: && {command}'

        process: subprocess.Popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return process