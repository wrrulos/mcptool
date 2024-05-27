import subprocess
import datetime
import base64
import shutil
import time
import os

from typing import Union
from mccolors import mcwrite
from loguru import logger

from ....utilities.minecraft.server.get_server import MCServerData, JavaServerData, BedrockServerData
from ....utilities.managers.language_manager import LanguageManager as LM
from ...managers.settings_manager import SettingsManager as SM
from ..text.text_utilities import TextUtilities
from ...path.mcptool_path import MCPToolPath
from ...constants import OS_NAME
from .jar import JarManager


class Fakeproxy:
    def __init__(self, process: subprocess.Popen, server_data: JavaServerData, target: str) -> None:
        self.process: subprocess.Popen = process
        self.server_data: JavaServerData = server_data
        self.target = target

    @logger.catch
    def configure(self) -> None:
        """
        Method to configure the fakeproxy
        """

        # Set the favicon of the fakeproxy if it exists or use the default one
        self._set_favicon()

        # Set the command prefix for the rpoisoner plugin
        self._set_command_prefix()

        # Remove old data file if it exists
        self._remove_data_file()

        # Show the fakeproxy data
        self._show_fakeproxy_data()

    @logger.catch
    def _show_fakeproxy_data(self) -> None:
        """
        Method to show the fakeproxy data
        """

        data_file_path: str = f'{MCPToolPath().get()}/proxies/fakeproxy/plugins/RPoisoner/data.txt'
        data_file_lines_number: int = 0

        while True:
            time.sleep(1)

            # Update the data for the fakeproxy (motd, players, etc.)
            self._update_fakeproxy_data()

            if not os.path.exists(data_file_path):
                continue

            with open(data_file_path, 'r', encoding='utf8') as file:
                data_file_lines: list = file.readlines()

                while True:
                    try:
                        # Get the last line of the data file
                        line = data_file_lines[data_file_lines_number].replace('\n', '')

                        player_data: list = line.split('/#-#/')
                        data_type: str = player_data[0]
                        username: str = player_data[1]
                        ip_address: str = player_data[2]
                        current_time: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        if data_type == '[CONNECTING]':
                            mcwrite(LM().get(['commands', 'fakeproxy', 'connected'])
                                .replace('%username%', username)
                                .replace('%ipAddress%', ip_address)
                                .replace('%time%', current_time)
                            )

                        if data_type == '[DISCONNECTING]':
                            mcwrite(LM().get(['commands', 'fakeproxy', 'disconnected'])
                                .replace('%username%', username)
                                .replace('%ipAddress%', ip_address)
                                .replace('%time%', current_time)
                            )

                        if data_type == '[CHAT]':
                            # Get the message from the player data
                            message: str = player_data[3]

                            mcwrite(LM().get(['commands', 'fakeproxy', 'chat'])
                                .replace('%username%', username)
                                .replace('%ipAddress%', ip_address)
                                .replace('%message%', message)
                                .replace('%time%', current_time)
                            )

                        if data_type == '[COMMAND]':
                            # Get the command from the player data
                            command: str = player_data[3]

                            mcwrite(LM().get(['commands', 'fakeproxy', 'command'])
                                .replace('%username%', username)
                                .replace('%ipAddress%', ip_address)
                                .replace('%command%', command)
                                .replace('%time%', current_time)
                            )

                        data_file_lines_number += 1

                    except IndexError:
                        break

    @logger.catch
    def _update_fakeproxy_data(self) -> None:
        """
        Method to update the fakeproxy data (motd, players, etc.)
        """

        server_data: Union[JavaServerData, BedrockServerData, None] = MCServerData(target=self.target, bot=False).get()

        if server_data is None:
            return

        if server_data.platform != 'Java':
            return

        rpoisoner_plugin_path: str = f'{MCPToolPath().get()}/proxies/fakeproxy/plugins/RPoisoner'
        motd_file_path: str = f'{rpoisoner_plugin_path}/settings/motd'
        version_file_path: str = f'{rpoisoner_plugin_path}/settings/version'
        protocol_file_path: str = f'{rpoisoner_plugin_path}/settings/protocol'
        online_players_file_path: str = f'{rpoisoner_plugin_path}/settings/onlinePlayers'
        max_players_file_path: str = f'{rpoisoner_plugin_path}/settings/maximumPlayers'
        samplePlayers_file_path: str = f'{rpoisoner_plugin_path}/settings/samplePlayers'

        # Set the motd of the fakeproxy
        with open(motd_file_path, 'w+', encoding='utf8') as file:
            file.truncate(0)
            file.write(TextUtilities.minimessage_colors(server_data.original_motd))

        # Set the version of the fakeproxy
        with open(version_file_path, 'w+', encoding='utf8') as file:
            file.truncate(0)
            file.write(TextUtilities.minimessage_colors(server_data.original_version))

        # Set the protocol of the fakeproxy
        with open(protocol_file_path, 'w+', encoding='utf8') as file:
            file.truncate(0)
            file.write(server_data.protocol)

        # Set the online players of the fakeproxy
        with open(online_players_file_path, 'w+', encoding='utf8') as file:
            file.truncate(0)
            file.write(server_data.connected_players)

        # Set the maximum players of the fakeproxy
        with open(max_players_file_path, 'w+', encoding='utf8') as file:
            file.truncate(0)
            file.write(server_data.max_players)

        # Set the sample players of the fakeproxy
        if server_data.player_list is not None and len(server_data.player_list) > 0:
            with open(samplePlayers_file_path, 'w+', encoding='utf8') as file:
                file.truncate(0)

                for player in server_data.player_list:
                    username: str = player['name']
                    uuid: str = player['id']
                    file.write(f'{username}/#-#/{uuid}\n')

    @logger.catch
    def _set_favicon(self) -> None:
        """
        Method to set the favicon of the fakeproxy
        """

        favicon_path: str = f'{MCPToolPath().get()}/proxies/fakeproxy/server-icon.png'

        if self.server_data.favicon is not None:
            try:
                with open(favicon_path, 'wb') as file:
                    file.truncate(0)
                    icon: Union[str, bytes] = self.server_data.favicon.replace('data:image/png;base64,', '')
                    icon = base64.b64decode(icon)
                    file.write(icon)

                return

            except Exception as e:
                logger.error(f'Error setting the favicon of the fakeproxy: {e}. Using the default favicon.')

        shutil.copy(f'{MCPToolPath().get()}/img/server-icon.png', favicon_path)

    @logger.catch
    def _set_command_prefix(self) -> None:
        """
        Method to set the command prefix for the rpoisoner plugin
        """

        command_prefix: str = SM().get(['proxyOptions', 'fakeproxyCommandPrefix'])

        if command_prefix == '':  # If the command prefix is empty, use the default one
            command_prefix = '..'

        command_prefix_file_path: str = f'{MCPToolPath().get()}/proxies/fakeproxy/plugins/RPoisoner/config/commandPrefix'

        if not os.path.exists(command_prefix_file_path):
            return

        with open(command_prefix_file_path, 'w+', encoding='utf8') as file:
            file.truncate(0)
            file.write(command_prefix)

    @logger.catch
    def _remove_data_file(self) -> None:
        """
        Method to remove the data file of the fakeproxy
        """

        data_file_path: str = f'{MCPToolPath().get()}/proxies/fakeproxy/plugins/RPoisoner/data.txt'

        if not os.path.exists(data_file_path):
            return

        os.remove(data_file_path)

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

        proxy_started: bool = self._read_output(process)

        if not proxy_started:
            process.kill()
            return

        if self.proxy == 'fakeproxy':
            Fakeproxy(process=process, server_data=server_data, target=self.target).configure()

        else:
            process.wait()

    @logger.catch
    def _read_output(self, process: subprocess.Popen) -> bool:
        """
        Method to read the output of the proxy

        Returns:
            bool: True if the proxy started successfully, False otherwise
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
                return False

            if 'Invalid or corrupt jarfile' in output_line:
                mcwrite(LM().get(['errors', 'invalidJarFile']))
                logger.error(f'Invalid or corrupt jarfile: {self.proxy}. Reason: {output_line}')
                return False

            if 'Unable to read/load/save your velocity.toml' in output_line:
                mcwrite(LM().get(['errors', 'velocityTomlError']))
                logger.error(f'Unable to read/load/save your velocity.toml: {output_line}')
                return False

            if 'Listening on' in output_line:
                return True

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

        if self.proxy == 'velocity' or self.proxy == 'fakeproxy':
            self.proxy_settings_path = f'{mcptool_path}/txt/{self.proxy}.config'
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

        # Set the proxy jar
        proxy_jar: str = 'velocity' if self.proxy == 'fakeproxy' else self.proxy

        # Check if the proxy exists. If not, download it
        JarManager(jar_name=proxy_jar, jar_path=self.proxy_path).check()

        if not os.path.exists(f'{self.proxy_path}/{proxy_jar}.jar'):
            mcwrite(LM().get(['errors', 'proxyJarNotFound']))
            logger.critical(f'Proxy jar not found: {self.proxy_path}/{proxy_jar}.jar')
            return None

        # Start the proxy
        command: str = f'cd {self.proxy_path} && java -jar {proxy_jar}.jar'

        if OS_NAME == 'windows':
            command = f'C: && {command}'

        process: subprocess.Popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return process
