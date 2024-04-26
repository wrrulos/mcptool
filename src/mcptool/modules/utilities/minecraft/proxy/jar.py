import requests
import os

from loguru import logger
from typing import Union

from ...path.mcptool_path import MCPToolPath
from ...managers.settings_manager import SettingsManager as SM


class JarManager:
    def __init__(self, jar_name: str, jar_path: str):
        self.jar_name = jar_name
        self.jar_path = jar_path
        
    @logger.catch
    def check(self) -> bool:
        """
        Method to check if the jar file exists
        """
        
        if not os.path.exists(self.jar_path):
            logger.error(f'Jar file not found: {self.jar_path}. Downloading it')
            self._download()
            self._replace_jar()

        self._get_latest_version()

        if self.latest_version_url is None:
            logger.error(f'Error while getting the latest version of the jar file -> {self.jar_name}')
            return

        if SM().get(f'{self.jar_name}Version') != self.latest_version_url:
            logger.info(f'Jar file already up to date -> {self.jar_name}')
            self._download()
            self._replace_jar()

    @logger.catch
    def _get_latest_version(self) -> Union[str, None]:
        """
        Method to get the latest version of the jar file

        Returns:
            str: The latest version of the jar file
        """

        logger.info(f'Getting latest version of the jar file -> {self.jar_name}')
        download_url: str = self._get_download_url()

        try:
            last_version: str = requests.get(download_url).json()['versions'][-1]
            latest_build: dict = requests.get(f'{download_url}/versions/{last_version}/builds/').json()['builds'][-1]
            build, name = latest_build['build'], latest_build['downloads']['application']['name']
            latest_version_url: str = f'https://api.papermc.io/v2/projects/waterfall/versions/{last_version}/builds/{build}/downloads/{name}'
            self.latest_version_url = latest_version_url
        
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            logger.error(f'Error while getting the latest version of the jar file -> {self.jar_name}. {e}')
            self.latest_version_url = None
    
    @logger.catch
    def _get_download_url(self) -> str:
        """
        Method to get the download url for the jar file

        Returns:
            str: The download url
        """
        
        if self.jar_name == 'velocity':
            return 'https://api.papermc.io/v2/projects/velocity'

        else:  # Waterfall
            return 'https://api.papermc.io/v2/projects/waterfal'
        
    @logger.catch
    def _download(self) -> bool:
        """
        Method to download the jar file

        Returns:
            bool: True if the download was successful, False otherwise
        """
        
        mcptool_path: str = MCPToolPath().get()
        jar_path: str = f'{mcptool_path}/jars/{self.jar_name}.jar'

        if os.path.exists(self.jar_path):
            os.remove(self.jar_path)

        with open(jar_path, 'wb') as f:
            try:
                f.truncate(0)
                response = requests.get(self.latest_version_url)
                f.write(response.content)
                logger.info(f'Jar file downloaded successfully -> {self.jar_name}')

            except requests.exceptions.RequestException as e:
                logger.error(f'Error while downloading the jar file -> {self.jar_name}. {e}')
                return False
            
            except Exception as e:
                logger.error(f'Error while downloading the jar file -> {self.jar_name}. {e}')
                return False
            
        return True
    
    @logger.catch
    def _replace_jar(self) -> bool:
        """
        Method to replace the jar file

        Returns:
            bool: True if the jar file was replaced successfully, False otherwise
        """
        
        try:
            for proxy in ['waterfall', 'velocity', 'fakeproxy']:
                if proxy == 'waterfall':
                    jar = 'waterfall'

                else:
                    jar = 'velocity'

                os.replace(
                    src=f'{MCPToolPath().get()}/jars/{jar}.jar', 
                    dst=f'{MCPToolPath().get()}/proxies/{proxy}/{jar}.jar'
                )

            logger.info(f'Jar file replaced successfully -> {self.jar_name}')
            return True
        
        except Exception as e:
            logger.error(f'Error while replacing the jar file -> {self.jar_name}. {e}')
            return False