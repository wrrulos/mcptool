from mccolors import mcwrite
from loguru import logger

from ..utilities.commands.validate import ValidateArgument
from ..utilities.scrapers.iphistory import DomainIPHistory
from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.ip.get_cloudflare_ips import GetCloudflareIps
from ..utilities.constants import SPACES


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'iphistory'
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

        if not ValidateArgument.is_domain(arguments[0]):
            mcwrite(LM.get('errors.invalidDomain'))
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

        ips: list = DomainIPHistory(domain=arguments[0]).get()

        if len(ips) == 0:
            mcwrite(LM.get('commands.iphistory.noIpHistory'))
            return

        cloudflare_ips: list = GetCloudflareIps().get(ips=ips)

        mcwrite(LM.get('commands.iphistory.ipHistoryFound'))

        # Print the IP history (cloudflare ips)
        for ip in ips:
            if ip in cloudflare_ips:
                mcwrite(f'{SPACES} &a&l• &d&l{ip} &8&l(&d&lCloudFlare&8&l)')

        # Print the IP history (non-cloudflare ips)
        for ip in ips:
            if ip not in cloudflare_ips:
                mcwrite(f'{SPACES} &a&l• &f&l{ip}')
