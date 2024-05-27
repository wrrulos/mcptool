import time

from loguru import logger
from mccolors import mcwrite

from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.virustotal.get_subdomains import GetSubdomains as GetSubdomainsVirustotal
from ..utilities.hackertarget.get_subdomains import GetSubdomains as GetSubdomainsHackerTarget
from ..utilities.ip.get_cloudflare_ips import GetCloudflareIps
from ..utilities.commands.validate import ValidateArgument
from ..utilities.constants import SPACES


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'resolver'
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]

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
            mcwrite(LM().get(['errors', 'invalidDomain']))
            return False

        return True

    @logger.catch
    def execute(self, arguments: list) -> None:
        """
        Method to execute the command

        Args:
            arguments (list): The arguments to execute the command
        """

        if not self.validate_arguments(arguments):
            return

        domain: str = arguments[0]

        mcwrite(LM().get(['commands', self.name, 'resolving']).replace('%domain%', domain))
        time.sleep(0.5)

        # Get the subdomains of the domain using VirusTotal API
        mcwrite(LM().get(['commands', self.name, 'gettingSubdomainsVirusTotal']))
        subdomains_virustotal: list = GetSubdomainsVirustotal().get_subdomains(domain=domain)

        # Get the subdomains of the domain using HackerTarget API
        mcwrite(LM().get(['commands', self.name, 'gettingSubdomainsHackerTarget']))
        subdomains_hackertarget: list = GetSubdomainsHackerTarget().get_subdomains(domain=domain)

        # Merge the subdomains
        subdomains: list = subdomains_virustotal + subdomains_hackertarget

        # Remove duplicates
        temp_dict = {}

        for item in subdomains:
            temp_dict[item[1]] = item

        # Get the subdomains list without duplicates
        subdomains_list = list(temp_dict.values())

        if len(subdomains_list) == 0:
            mcwrite(LM().get(['errors', 'noSubdomainsFoundResolver']))
            return

        # Get ips from the subdomains
        ips = [subdomain[1] for subdomain in subdomains_list]

        # Get Cloudflare IPs from the list of IPs
        cloudflare_ips = GetCloudflareIps().get(ips=ips)

        print('')

        # Print the subdomains with the cloudflare ips
        for subdomain, ip in subdomains_list:
            if ip in cloudflare_ips:
                mcwrite(f'{SPACES} &a&l• &d&l{ip} &8&l(&a&l{subdomain}&8&l) &8&l(&d&lCloudFlare&8&l)')

        # Print the subdomains with unknown ips
        for subdomain, ip in subdomains_list:
            if ip not in cloudflare_ips:
                mcwrite(f'{SPACES} &a&l• &f&l{ip} &8&l(&a&l{subdomain}&8&l)')

        mcwrite(LM().get(['commands', self.name, 'done'])
            .replace('%domain%', domain)
            .replace('%subdomainsAmount%', str(len(subdomains_list))
        ))