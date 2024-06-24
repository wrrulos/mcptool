import subprocess
import requests
import sys
import os

from loguru import logger
from mccolors import mcwrite

from ..constants import OS_NAME, GITHUB_REPOSITORY


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

        folder_name: str = 'MCPToolData'

        if self.system == 'nt':
            path: str = os.path.abspath(os.path.join(os.getenv('APPDATA'), folder_name))

        else:
            path: str = os.path.abspath(os.path.join(os.getenv('HOME'), '.config', folder_name))

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
                    mcwrite(f'&8&l[&a&lINFO&8&l] &f&lDownloading {url["path"]}')
                    logger.info(f'Downloading {url["path"]}')
                    self.download_file(url['url'], url['path'])

            if not os.path.exists(os.path.join(self.get(), 'node_modules')):
                logger.info('Installing node modules')
                mcwrite('&8&l[&a&lINFO&8&l] &f&lInstalling node modules...')
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
            response: requests.Response = requests.get(url)

            if response.status_code != 200:
                mcwrite(f'&8&l[&c&lERROR&8&l] &f&lError downloading file: {path}')
                logger.error(f'Error downloading file: {response.status_code} from {url}')
                return

            with open(path, 'wb') as file:
                if response.content is None:
                    mcwrite(f'&8&l[&c&lERROR&8&l] &f&lError downloading file: {path}')
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
                'url': f'{GITHUB_REPOSITORY}settings.json',
                'path': os.path.abspath(os.path.join(self.get(), 'settings.json'))
            },
            'bruteforce_settings': {
                'url': f'{GITHUB_REPOSITORY}bruteforce_settings.json',
                'path': os.path.abspath(os.path.join(self.get(), 'bruteforce_settings.json'))
            },
            'sendcmd_settings': {
                'url': f'{GITHUB_REPOSITORY}sendcmd_settings.json',
                'path': os.path.abspath(os.path.join(self.get(), 'sendcmd_settings.json'))
            },
            'mcserver-scrapper': {
                'url': f'{GITHUB_REPOSITORY}mcserver-scrapper.json',
                'path': os.path.abspath(os.path.join(self.get(), 'mcserver-scrapper.json'))
            },
            # Packages
            "package": {
                "url": f"{GITHUB_REPOSITORY}package.json",
                "path": os.path.abspath(os.path.join(self.get(), "package.json"))
            },
            # Languages
            'language_en': {
                'url': f'{GITHUB_REPOSITORY}languages/en.json',
                'path': os.path.abspath(os.path.join(self.get(), 'languages', 'en.json'))
            },
            'language_es': {
                'url': f'{GITHUB_REPOSITORY}languages/es.json',
                'path': os.path.abspath(os.path.join(self.get(), 'languages', 'es.json'))
            },
            'language_tr': {
                'url': f'{GITHUB_REPOSITORY}languages/tr.json',
                'path': os.path.abspath(os.path.join(self.get(), 'languages', 'tr.json'))
            },
            # Scripts
            'bot_script': {
                'url': f'{GITHUB_REPOSITORY}scripts/bot.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'bot.mjs'))
            },
            'utilities_script': {
                'url': f'{GITHUB_REPOSITORY}scripts/utilities.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'utilities.mjs'))
            },
            'server_response_script': {
                'url': f'{GITHUB_REPOSITORY}scripts/server_response.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'server_response.mjs'))
            },
            'brute_auth_script': {
                'url': f'{GITHUB_REPOSITORY}scripts/brute_auth.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'brute_auth.mjs'))
            },
            'connect_script': {
                'url': f'{GITHUB_REPOSITORY}scripts/connect.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'connect.mjs'))
            },
            'sendcmd_script': {
                'url': f'{GITHUB_REPOSITORY}scripts/sendcmd.mjs',
                'path': os.path.abspath(os.path.join(self.get(), 'scripts', 'sendcmd.mjs'))
            },
            # Txt files
            "usernames": {
                "url": f'{GITHUB_REPOSITORY}txt/bot_username.txt',
                "path": os.path.abspath(os.path.join(self.get(), 'txt', 'bot_username.txt'))
            },
            "fakeproxy": {
                "url": f'{GITHUB_REPOSITORY}txt/fakeproxy.config',
                "path": os.path.abspath(os.path.join(self.get(), 'txt', 'fakeproxy.config'))
            },
            "waterfall_config": {
                "url": f'{GITHUB_REPOSITORY}txt/waterfall.config',
                "path": os.path.abspath(os.path.join(self.get(), 'txt', 'waterfall.config'))
            },
            "velocity_config": {
                "url": f'{GITHUB_REPOSITORY}txt/velocity.config',
                "path": os.path.abspath(os.path.join(self.get(), 'txt', 'velocity.config'))
            },
            # Scanners
            "qubo_scanner": {
                "url": f'{GITHUB_REPOSITORY}scanners/qubo.jar',
                "path": os.path.abspath(os.path.join(self.get(), "scanners", "qubo.jar"))
            },
            # Proxies directory
            "proxies/waterfall": {
                "url": f'{GITHUB_REPOSITORY}.directory',
                "path": os.path.abspath(os.path.join(self.get(), "proxies", "waterfall", ".directory"))
            },
            "proxies/velocity": {
                "url": f'{GITHUB_REPOSITORY}.directory',
                "path": os.path.abspath(os.path.join(self.get(), "proxies", "velocity", ".directory"))
            },
            "proxies/fakeproxy": {
                "url": f'{GITHUB_REPOSITORY}.directory',
                "path": os.path.abspath(os.path.join(self.get(), "proxies", "fakeproxy", ".directory"))
            },
            "jar_directory": {
                "url": f'{GITHUB_REPOSITORY}.directory',
                "path": os.path.abspath(os.path.join(self.get(), "jars", '.directory'))
            },
            # Forwarding secrets
            'forwarding.secret_velocity': {
                'url': f'{GITHUB_REPOSITORY}txt/forwarding.secret',
                'path': os.path.abspath(os.path.join(self.get(), 'proxies', 'velocity', 'forwarding.secret'))
            },
            'forwarding.secret_fakeproxy': {
                'url': f'{GITHUB_REPOSITORY}txt/forwarding.secret',
                'path': os.path.abspath(os.path.join(self.get(), 'proxies', 'fakeproxy', 'forwarding.secret'))
            },
            # Jar plugins for the proxies
            'mcptool_velocity_plugin': {
                'url': 'https://github.com/wrrulos/mcptool-velocity/releases/download/v1.1/MCPTool-1.1-SNAPSHOT.jar',
                'path': os.path.abspath(os.path.join(self.get(), 'proxies', 'velocity', 'plugins', 'MCPTool-1.1-SNAPSHOT.jar'))
            },
            'mcptool_fakeproxy_plugin': {
                'url': f'{GITHUB_REPOSITORY}jar/RPoisoner-1.1-SNAPSHOT.jar',
                'path': os.path.abspath(os.path.join(self.get(), 'proxies', 'fakeproxy', 'plugins', 'RPoisoner-1.1-SNAPSHOT.jar'))
            },
            'mcptool_waterfall_plugin': {
                'url': 'https://github.com/wrrulos/RBungeeExploit/releases/download/v1.0/RBungeeExploit-1.0.jar',
                'path': os.path.abspath(os.path.join(self.get(), 'proxies', 'waterfall', 'plugins', 'RBungeeExploit-1.0.jar'))
            },
            # Imgs
            'server-icon': {
                'url': f'{GITHUB_REPOSITORY}img/server-icon.png',
                'path': os.path.abspath(os.path.join(self.get(), 'img', 'server-icon.png'))
            },
            'icon': {
                'url': f'{GITHUB_REPOSITORY}img/icon.ico',
                'path': os.path.abspath(os.path.join(self.get(), 'img', 'icon.ico'))
            }
        }
