import json
import requests
import threading

from typing import Union
from bs4 import BeautifulSoup, element
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
from mccolors import mcwrite

from ..minecraft.server import JavaServerData, BedrockServerData
from ..path.mcptool_path import MCPToolPath
from ..minecraft.server.get_server import ServerData
from ..minecraft.server.show_server import ShowMinecraftServer
from ...utilities.managers.language_utils import LanguageUtils as LM


class MinecraftServerScrapper:
    @logger.catch
    def __init__(self) -> None:
        mcptool_path: str = MCPToolPath().get()
        self.file: str = open(f'{mcptool_path}/mcserver-scrapper.json', 'r').read()
        self.headers: dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.cookies: dict = {'cookie_name': 'cookie_value'}
        self.servers: dict = json.loads(self.file)
        self.filters: dict = {
            'filterByDescription': False,
            'filterByOnlinePlayers': False,
            'filterByProtocol': False,
            'onlyBotCanJoin': False,
            'description': '',
            'onlinePlayers': 0,
            'protocol': 0
        }
        self.stop_event = threading.Event()
        self.server_list: list = []

    @logger.catch
    def get(self) -> dict:
        """
        Method to get the Minecraft server scrapper data

        Returns:
            dict: The Minecraft server scrapper data
        """

        mcwrite(LM.get('commands.websearch.searchingInWebs'))

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures: list = []

            for server_page in self.servers:
                url: str = server_page['url']
                pages: int = int(server_page['pages'])
                mcwrite(LM.get('commands.websearch.searchingInPage').replace('%page%', server_page['name']))

                for i in range(1, pages + 1):
                    if self.stop_event.is_set():
                        return

                    url_with_page: str = url.replace('#', str(i))
                    futures.append(executor.submit(self.scrape_page, url_with_page, server_page))

            for future in as_completed(futures):
                if self.stop_event.is_set():
                    return

                future.result()

    @logger.catch
    def scrape_page(self, url_with_page: str, server_page: dict) -> None:
        """
        Method to scrape a single page

        Args:
            url_with_page (str): The URL with the page number
            server_page (dict): The server page data
        """

        if self.stop_event.is_set():
            return

        page: Union[BeautifulSoup, None] = self.read_page(url=url_with_page)

        if page is not None:
            self.get_servers_in_page(page=page, server_page=server_page, method=server_page['method'])

    @logger.catch
    def read_page(self, url: str) -> BeautifulSoup:
        """
        Method to read the page

        Args:
            url (str): The URL to read

        Returns:
            BeautifulSoup: The page content
        """

        try:
            response = requests.get(url=url, headers=self.headers, cookies=self.cookies, timeout=5)

            if response.status_code != 200:
                return None

            return BeautifulSoup(response.content, 'html.parser')

        except requests.RequestException as e:
            logger.error(f'Error reading page: {e}')
            return None

    @logger.catch
    def get_servers_in_page(self, page: BeautifulSoup, server_page: dict, method: str) -> None:
        """
        Method to get the servers in the page

        Args:
            page (BeautifulSoup): The page content
            server_page (dict): The server page
        """

        html_tags: element.ResultSet = page.find_all(server_page['find_all']['tag'], class_=server_page['find_all']['class'])

        for server in html_tags:
            if self.stop_event.is_set():
                break

            if method == 'text':
                ip: Union[str, None] = self._extract_server_text_method(server=server, server_page=server_page)

            if ip is None:
                continue

            if ip in self.server_list:
                continue

            server_data: Union[JavaServerData, BedrockServerData, None] = ServerData(target=ip).get_data()

            if server_data is not None:
                if self.filters['onlyBotCanJoin']:
                    if server_data.bot_output != '&a&lConnected':
                        continue

                if self.filters['filterByDescription']:
                    if str(self.filters['description']).lower() not in server_data.motd.lower():
                        continue

                if self.filters['filterByOnlinePlayers']:
                    if int(server_data.connected_players) < self.filters['onlinePlayers']:
                        continue

                if self.filters['filterByProtocol']:
                    if int(server_data.protocol) != self.filters['protocol']:
                        continue

                ShowMinecraftServer.show(server_data)

            self.server_list.append(ip)

    @logger.catch
    def _extract_server_text_method(self, server: BeautifulSoup, server_page: dict) -> Union[str, None]:
        """
        Method to extract the server using the text method

        Args:
            server (BeautifulSoup): The server
            server_page (dict): The server page

        Returns:
            Union[str, None]: The server
        """

        try:
            server: Union[str, None] = server.find(server_page['find']['tag'], class_=server_page['find']['class']).text
            return server

        except AttributeError:
            return None

    @logger.catch
    def set_default_filters(self) -> None:
        """
        Method to set the default filters
        """

        self.filters = {
            'filterByDescription': False,
            'filterByOnlinePlayers': False,
            'filterByProtocol': False,
            'onlyBotCanJoin': False,
            'description': '',
            'onlinePlayers': 0,
            'protocol': 0
        }

    @logger.catch
    def restore(self) -> None:
        """
        Method to restore the scrapper
        """
        self.stop_event.clear()
        self.set_default_filters()

    @logger.catch
    def stop(self) -> None:
        """
        Method to signal the scrapper to stop
        """
        self.stop_event.set()
