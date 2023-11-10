import subprocess
import datetime
import time

from src.proxy.fakeproxy import FakeProxy
from src.decoration.paint import paint
from src.managers.json_manager import JsonManager
from src.utilities.file_utilities import FileUtilities
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData
from src.managers.log_manager import LogManager


class ProxyLauncher:
    @staticmethod
    def start_proxy(proxy_type, address, velocity_mode=None):
        """
        Start a Minecraft proxy server of the specified type.

        Args:
            proxy_type (str): The type of proxy to start ('velocity', 'fakeproxy', 'waterfall').
            address (str): The server IP address or domain to connect to.
            velocity_mode (str, optional): The velocity mode for 'velocity' proxy type (default is None).

        This method configures and starts a Minecraft proxy server of the specified type. It reads the proxy configuration
        file, replaces placeholders with specific values, and launches the proxy server. Depending on the proxy type,
        additional setup and configuration may be performed.
        """

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = ''
        
        # Inform the user that proxy configuration is in progress.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "configuring"])}')
        time.sleep(0.5)
        
        server_data = GetMinecraftServerData.get_data(address, bot=False, clean_data=False)

        if server_data is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')
            return None
        
        if JsonManager.get(["proxyConfig", "convertDomainToIP"]):
            address = server_data['ip_port']

        # Define the path to the proxy configuration file.
        proxy_config_path = f'./mcptool_files/proxy/settings/{proxy_type}.config'

        # Read the proxy configuration file.
        with open(proxy_config_path, 'r', encoding='utf8') as f:
            proxy_config = f.read()

        # Replace placeholders in the proxy configuration with specific values.
        proxy_config, proxy_port = ProxyLauncher.replace_proxy_variables(proxy_type, proxy_config, address, velocity_mode)

        # Handle different proxy types ('velocity', 'fakeproxy', 'waterfall').
        if proxy_type in ['velocity', 'fakeproxy']:
            if JsonManager.get('logs'):
                log_file = LogManager.create_log_file(proxy_type)

                if proxy_type == 'velocity':
                    LogManager.write_log(log_file, 'fakeproxy', f'{current_time} Target: {address}\n')

                else:
                    LogManager.write_log(log_file, 'fakeproxy', f'{current_time} Target: {address} (Forwading mode: {velocity_mode})\n')

            # Write the modified configuration to a Velocity TOML file.
            FileUtilities.write_file(f'./mcptool_files/proxy/jar/{proxy_type}/velocity.toml', proxy_config, 'w+', True)

            # Perform additional setup for the 'fakeproxy' type.
            if proxy_type == 'fakeproxy':
                if FakeProxy.setup(address) is False:
                    return None

            # Inform the user that the proxy server is starting.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "starting"])}')

            # Launch the proxy server using a subprocess.
            subprocess.Popen(f'cd ./mcptool_files/proxy/jar/{proxy_type} && {JsonManager.get(["proxyConfig", "velocityCommand"])}', stdout=subprocess.PIPE, shell=True)

        else:
            if JsonManager.get('logs'):
                log_file = LogManager.create_log_file('waterfall')
                LogManager.write_log(log_file, 'waterfall', f'{current_time} Target: {address}\n')

            # Write the modified configuration to a Waterfall YAML file.
            FileUtilities.write_file(f'./mcptool_files/proxy/jar/{proxy_type}/config.yml', proxy_config, 'w+', True)

            # Inform the user that the proxy server is starting.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "starting"])}')

            # Launch the proxy server using a subprocess.
            subprocess.Popen(f'cd ./mcptool_files/proxy/jar/{proxy_type} && {JsonManager.get(["proxyConfig", "waterfallCommand"])}', stdout=subprocess.PIPE, shell=True)
        
        time.sleep(5)

        if not CheckUtilities.check_local_port(int(proxy_port)):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["proxyMessages", "proxyServerNotStartup"])}')
            return
        
        # Display information about the started proxy server.
        if proxy_type == 'fakeproxy':
            if GetUtilities.get_ip_ngrok() is not None:
                paint(f"""\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["proxyMessages", "proxyServerStarted"]).replace("[0]", f"127.0.0.1:{proxy_port} &f&l(&d{GetUtilities.get_ip_ngrok()}&f&l)")}""")
            
            else:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "ipNgrokError"])}')
                paint(f"""\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["proxyMessages", "proxyServerStarted"]).replace("[0]", f"127.0.0.1:{proxy_port}")}""")
        
        else:
            paint(f"""\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["proxyMessages", "proxyServerStarted"]).replace("[0]", f"127.0.0.1:{proxy_port}")}""")

        # Show additional data if the proxy type is 'fakeproxy'.
        if proxy_type == 'fakeproxy':
            FakeProxy.show_data(address, log_file)

        else:
            while True:
                time.sleep(1)
    
    @staticmethod
    def replace_proxy_variables(proxy_type, proxy_config, address, velocity_mode):
        """
        Replace placeholders in a proxy configuration string with specific values.

        Args:
            proxy_type (str): The type of proxy ('fakeproxy', 'velocity', 'waterfall').
            proxy_config (str): The proxy configuration string with placeholders.
            address (str): The address to replace '[[ADDRESS]]'.
            velocity_mode (str): The velocity mode to replace '[[MODE]]'.

        Returns:
            str: The modified proxy configuration string with placeholders replaced.
        """
        
        # Replace '[[ADDRESS]]' placeholder with the provided address.
        if '[[ADDRESS]]' in proxy_config:
            proxy_config = proxy_config.replace('[[ADDRESS]]', address)

        # Replace '[[PORT]]' placeholder based on the proxy type.
        if '[[PORT]]' in proxy_config:
            if proxy_type == 'fakeproxy':
                port = JsonManager.get(['proxyConfig', 'fakeProxyPort'])

            elif proxy_type == 'velocity':
                port = JsonManager.get(['proxyConfig', 'velocityPort'])
                
            else:
                port = JsonManager.get(['proxyConfig', 'waterfallPort'])

            proxy_config = proxy_config.replace('[[PORT]]', port)

        else:
            port = "2"

        # Replace '[[MODE]]' placeholder with the provided velocity mode.
        if '[[MODE]]' in proxy_config:
            proxy_config = proxy_config.replace('[[MODE]]', velocity_mode)

        return proxy_config, port