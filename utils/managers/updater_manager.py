import json
import os
import requests
import shutil
import socket
import zipfile

from utils.managers.config_manager import config_manager


class Updater:
    def __init__(self) -> None:
        pass

    def download(self, file, url, location):
        """
        Download the specified file.

        Args:
            file (str): The name of the file to be downloaded.
            url (str): The URL from which to download the file.
            location (str): The location to save the downloaded file.

        Returns:
            bool: True if the download is successful, False if the process is interrupted by a KeyboardInterrupt.
        """

        try:
            if os.path.exists(location):
                shutil.rmtree(location)

            os.mkdir(location)

            with open(f'{location}/{file}', 'wb') as f:
                file = requests.get(url)
                f.write(file.content)
                return True

        except KeyboardInterrupt:
            return False

    def extracting(self, file, location):
        """
        Extracts the specified .zip file.

        Args:
            file (str): The path to the .zip file to be extracted.
            location (str): The location to extract the contents of the .zip file.

        Returns:
            bool: True if the extraction is successful, False otherwise.
        """

        with zipfile.ZipFile(file, mode="r") as archive:
            archive.extractall(location)
            return True

    def check_mcptool_updates(self):
        """
        Check if there is a new version of MCPTool.

        Returns:
            bool: True if a new version is available, False otherwise.
        """

        try:
            js = json.loads(requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/settings/config.json').text)
            current_version = config_manager.config['currentVersion'].split('///')[0]
            last_version = js['currentVersion'].split('///')[0]
            return int(last_version) != int(current_version)

        except TypeError:
            return True

        except (socket.gaierror, socket.timeout, requests.ConnectionError, requests.ConnectTimeout, KeyboardInterrupt):
            return False

    def check_waterfall_update(self):
        """
        Check if a new version of waterfall is available.

        Returns:
            str or None: The URL of the latest Velocity version download if an update is available,
            None otherwise.
        """

        try:
            last_version = requests.get('https://api.papermc.io/v2/projects/waterfall').json()['versions'][-1]
            latest_build = requests.get(f'https://api.papermc.io/v2/projects/waterfall/versions/{last_version}/builds/').json()['builds'][-1]
            build, name = latest_build['build'], latest_build['downloads']['application']['name']
            url = f'https://api.papermc.io/v2/projects/waterfall/versions/{last_version}/builds/{build}/downloads/{name}'

            if config_manager.config['proxyConfig']['waterfallVersion'] != url:
                config_manager.config['proxyConfig']['waterfallVersion'] = url
                config_manager.update_settings(config_manager.config)
                return url
    
        except (socket.gaierror, socket.timeout, requests.ConnectionError, requests.ConnectTimeout, KeyboardInterrupt):
            return
        
    def check_velocity_update(self):
        """
        Check if a new version of Velocity is available.

        Returns:
            str or None: The URL of the latest Velocity version download if an update is available,
            None otherwise.
        """

        try:
            last_version = requests.get('https://api.papermc.io/v2/projects/velocity').json()['versions'][-1]
            latest_build = requests.get(f'https://api.papermc.io/v2/projects/velocity/versions/{last_version}/builds/').json()['builds'][-1]
            build, name = latest_build['build'], latest_build['downloads']['application']['name']
            url = f'https://api.papermc.io/v2/projects/velocity/versions/{last_version}/builds/{build}/downloads/{name}'

            if config_manager.config['proxyConfig']['velocityVersion'] != url:
                config_manager.config['proxyConfig']['velocityVersion'] = url
                config_manager.update_settings(config_manager.config)
                return url
    
        except (socket.gaierror, socket.timeout, requests.ConnectionError, requests.ConnectTimeout, KeyboardInterrupt):
            return