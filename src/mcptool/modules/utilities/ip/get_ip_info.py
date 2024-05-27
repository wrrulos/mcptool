import requests
import socket

from typing import Union
from loguru import logger


class IPInfoFormat:
    def __init__(self, continent: Union[str, None], continent_code: Union[str, None], country: Union[str, None], country_code: Union[str, None], region: Union[str, None], region_name: Union[str, None], city: Union[str, None], timezone: Union[str, None], isp: Union[str, None], org: Union[str, None], domains: list) -> None:
        self.continent: Union[str, None] = continent
        self.continent_code: Union[str, None] = continent_code
        self.country: Union[str, None] = country
        self.country_code: Union[str, None] = country_code
        self.region: Union[str, None] = region
        self.region_name: Union[str, None] = region_name
        self.city: Union[str, None] = city
        self.timezone: Union[str, None] = timezone
        self.isp: Union[str, None] = isp
        self.org: Union[str, None] = org
        self.domains: list = []


class IPInfo:
    def __init__(self, ip_address: str, reverse: bool=False) -> None:
        self.ip_address = ip_address
        self.reverse = reverse
        self.domains: list = []

    @logger.catch
    def get_info(self) -> IPInfoFormat:
        """
        Get the information of the IP address

        Returns:
            IPInfoFormat: The information of the IP address
        """

        try:
            # Get the information of the IP address
            r = requests.get(f'http://ip-api.com/json/{self.ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,timezone,isp,org,as,asname,reverse,query')
            ip_address_information: dict = r.json()

            # Check if the status is not success
            if ip_address_information['status'] != 'success':
                return None

            # Check if the reverse DNS lookup is enabled
            if self.reverse:
                try:
                    self.domains: list = socket.gethostbyaddr(self.ip_address)[0]

                except socket.herror:
                    pass

            return IPInfoFormat(
                continent=ip_address_information['continent'],
                continent_code=ip_address_information['continentCode'],
                country=ip_address_information['country'],
                country_code=ip_address_information['countryCode'],
                region=ip_address_information['regionName'],
                region_name=ip_address_information['region'],
                city=ip_address_information['city'],
                timezone=ip_address_information['timezone'],
                isp=ip_address_information['isp'],
                org=ip_address_information['org'],
                domains=self.domains
            )

        except requests.exceptions.RequestException as e:
            return None
