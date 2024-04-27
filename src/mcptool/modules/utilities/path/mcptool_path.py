import subprocess
import requests
import sys
import os

from loguru import logger
from mccolors import mcwrite

from ..constants import OS_NAME


class MCPToolPath:
    def __init__(self) -> None:
        self.system: str = os.name
        self.urls: dict = self._get_urls()

    def get(self) -> str:
        """
        Method to get the path of the MCPTool folder
        and create it if it doesn't exist

        Returns:
            str: Path of the MCPTool folder
        """

        if self.system == 'nt':
            path = os.path.abspath(os.path.join(os.getenv('APPDATA'), 'MCPTool'))

        else:
            path = os.path.abspath(os.path.join(os.getenv('HOME'), '.config', 'mcptool'))

        if not os.path.exists(path):
            logger.info(f'Creating MCPTool folder in {path}')
            os.makedirs(os.path.join(path), exist_ok=True)

        return path
    
    def check_files(self) -> None:
        """
        Method to check if the files exist and 
        download them if they don't
        """

        try:
            for url in self.urls.values():
                if not os.path.exists(url['path']):
                    mcwrite(f'&a&lDownloading {url["path"]}')
                    logger.info(f'Downloading {url["path"]}')
                    self.download_file(url['url'], url['path'])

            if not os.path.exists(os.path.join(self.get(), 'node_modules')):
                logger.info('Installing node modules')
                mcwrite('&a&lInstalling node modules')
                command: str = f'cd {self.get()} && npm install'

                if OS_NAME == 'windows':
                    command = f'C: && {command}'

                subprocess.run(command, shell=True)
        
        except KeyboardInterrupt:
            sys.exit(0)

    def download_file(self, url: str, path: str) -> None:
        """
        Method to download the file

        Args:
            url (str): URL of the file
            path (str): Path to save the file
        """

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            response = requests.get(url)

            if response.status_code != 200:
                mcwrite(f'&cError downloading file: {path}')
                logger.error(f'Error downloading file: {response.status_code}')
                return

            with open(path, 'wb') as file:
                if response.content is None:
                    mcwrite(f'&cError downloading file: {path}')
                    logger.error(f'Error downloading file: {response.content}')
                    return

                file.write(response.content)
        
        except Exception as e:
            logger.error(f'Error downloading file: {e}')

    def _get_urls(self) -> dict:
        """
        Method to get the URLs of the files

        Returns:
            dict: URLs of the files
        """
        
        return {
            # Settings
            'settings': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/settings.json',
                'path': os.path.abspath(os.path.join(self.get(), 'settings.json'))
            },
            'bruteforce_settings': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/bruteforce_settings.json',
                'path': os.path.abspath(os.path.join(self.get(), 'bruteforce_settings.json'))
            },
            'sendcmd_settings': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/sendcmd_settings.json',
                'path': os.path.abspath(os.path.join(self.get(), 'sendcmd_settings.json'))
            },
            # Packages
            "package": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/package.json",
                "path": os.path.abspath(os.path.join(self.get(), "package.json"))
            },
            # Languages
            'language_en': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/languages/en.json',
                'path': os.path.abspath(os.path.join(self.get(), 'languages', 'en.json'))
            },
            # Scripts
            'bot_script': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/scripts/bot.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'bot.mjs'))
            },
            'utilities_script': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/scripts/utilities.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'utilities.mjs'))
            },
            'server_response_script': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/scripts/server_response.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'server_response.mjs'))
            },
            'brute_auth_script': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/scripts/brute_auth.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'brute_auth.mjs'))
            },
            'connect_script': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/scripts/connect.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'connect.mjs'))
            },
            'sendcmd_script': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/scripts/sendcmd.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'sendcmd.mjs'))
            },
            # Txt files
            "usernames": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/txt/usernames.txt",
                "path": os.path.abspath(os.path.join(self.get(), 'txt', 'usernames.txt'))
            },
            "fakeproxy": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/txt/fakeproxy.config",
                "path": os.path.abspath(os.path.join(self.get(), 'txt', 'fakeproxy.config'))
            },
            "waterfall_config": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/txt/waterfall.config",
                "path": os.path.abspath(os.path.join(self.get(), 'txt', 'waterfall.config'))
            },
            "velocity_config": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/txt/velocity.config",
                "path": os.path.abspath(os.path.join(self.get(), 'txt', 'velocity.config'))
            },
            # Scanners
            "qubo_scanner": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/scanners/qubo.jar",
                "path": os.path.abspath(os.path.join(self.get(), "scanners", "qubo.jar"))
            },
            # Proxies directory
            "proxies/waterfall": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/.directory",
                "path": os.path.abspath(os.path.join(self.get(), "proxies", "waterfall", ".directory"))
            },
            "proxies/velocity": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/.directory",
                "path": os.path.abspath(os.path.join(self.get(), "proxies", "velocity", ".directory"))
            },
            "proxies/fakeproxy": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/.directory",
                "path": os.path.abspath(os.path.join(self.get(), "proxies", "fakeproxy", ".directory"))
            },
            "jar_directory": {
                "url": "https://raw.githubusercontent.com/wrrulos/MCPTool/development/.directory",
                "path": os.path.abspath(os.path.join(self.get(), "jars", '.directory'))
            },
            'forwarding.secret_velocity': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/txt/forwarding.secret',
                'path': os.path.abspath(os.path.join(self.get(), 'proxies', 'velocity', 'forwarding.secret'))
            },
            'forwarding.secret_fakeproxy': {
                'url': 'https://raw.githubusercontent.com/wrrulos/MCPTool/development/src/txt/forwarding.secret',
                'path': os.path.abspath(os.path.join(self.get(), 'proxies', 'fakeproxy', 'forwarding.secret'))
            },
        }