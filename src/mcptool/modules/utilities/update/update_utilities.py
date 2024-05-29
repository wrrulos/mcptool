import requests

from loguru import logger
from plyer import notification

from ..path.mcptool_path import MCPToolPath


class UpdateUtilities:
    @staticmethod
    @logger.catch
    def update_available(VERSION: str, GITHUB_REPOSITORY: str):
        """
        Method to check if an update is available

        Returns:
            bool: True if an update is available, False otherwise
        """

        try:
            response: requests.Response = requests.get(f'{GITHUB_REPOSITORY}settings.json')

            if response.status_code != 200:
                return False

            settings = response.json()

            if settings['version'] != VERSION:
                notification.notify(
                    title='MCPTool Update Available',
                    message=f'An update is available for MCPTool! Please visit the Website to download the latest version.',
                    app_name='MCPTool',
                    app_icon=f'{MCPToolPath().get()}/img/icon.ico',
                    timeout=10
                )

            return settings['version'] != VERSION

        except Exception as e:
            logger.warning(f'Error checking for updates: {e}')
            return False
