from typing import Union
from mccolors import mcwrite
from loguru import logger

from ..utilities.commands.validate import ValidateArgument
from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.ip.get_ip_info import IPInfo, IPInfoFormat


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'ipinfo'
        self.arguments: list = [i for i in LM.get(f'commands.{self.name}.arguments')]

    @logger.catch
    def validate_arguments(self, arguments: list) -> bool:
        """
        Method to validate the arguments

        Args:
            arguments (list): The arguments to validate

        Returns:
            bool: True if the arguments are valid, False otherwise
        """

        if not ValidateArgument.validate_arguments_length(command_name=self.name, command_arguments=self.arguments, user_arguments=arguments):
            return False

        if not ValidateArgument.is_ip_address(arguments[0]):
            mcwrite(LM.get('errors.invalidIpFormat'))
            return False

        return True

    @logger.catch
    def execute(self, arguments: list) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        # Validate the arguments
        if not self.validate_arguments(arguments):
            return

        # Get the player data
        mcwrite(LM.get(f'commands.{self.name}.gettingIpData'))

        # Get the IP address information
        ip_info: Union[IPInfoFormat, None] = IPInfo(ip_address=arguments[0]).get_info()

        if ip_info is None:
            mcwrite(LM.get(f'commands.{self.name}.error'))
            return

        # Print the IP address information
        mcwrite(LM.get(f'commands.{self.name}.continent').replace('%continent%', ip_info.continent).replace('%continentCode%', ip_info.continent_code))
        mcwrite(LM.get(f'commands.{self.name}.country').replace('%country%', ip_info.country).replace('%countryCode%', ip_info.country_code))
        mcwrite(LM.get(f'commands.{self.name}.region').replace('%region%', ip_info.region).replace('%regionName%', ip_info.region_name))
        mcwrite(LM.get(f'commands.{self.name}.city').replace('%city%', ip_info.city))
        mcwrite(LM.get(f'commands.{self.name}.timezone').replace('%timezone%', ip_info.timezone))
        mcwrite(LM.get(f'commands.{self.name}.isp').replace('%isp%', ip_info.isp))
        mcwrite(LM.get(f'commands.{self.name}.organization').replace('%organization%', ip_info.org))
