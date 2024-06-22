import requests
import re

from mccolors import mcwrite

from ..managers.language_utils import LanguageUtils as LM


class DomainIPHistory:
    def __init__(self, domain: str):
        self.domain: str = domain
        self.url: str = f'https://viewdns.info/iphistory/?domain={self.domain}'
        self.headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.ip_pattern: str = r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>'

    def get(self):
        """
        Get the IP history of a domain.

        Returns:
            list: The IP history of a domain
        """

        try:
            mcwrite(LM.get('commands.iphistory.gettingIpHistory'))
            response: requests.Response = requests.get(url=self.url, headers=self.headers)

            if response.status_code != 200:
                mcwrite(LM.get('commands.iphistory.noIpHistory'))
                return []

            ips: list = re.findall(self.ip_pattern, response.text)
            return ips

        except requests.exceptions.RequestException:
            mcwrite(LM.get('errors.endpointConnectionError'))
            return
