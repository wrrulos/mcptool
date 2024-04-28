import time

from loguru import logger
from mccolors import mcwrite

from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.dns.get_dns_records import GetDNSRecords
from ..utilities.commands.validate import ValidateArgument
from ..utilities.constants import SPACES


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'dnslookup'
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

        mcwrite(LM().get(['commands', self.name, 'lookingUp']).replace('%domain%', domain))
        time.sleep(0.5)
        
        dns_records: list = GetDNSRecords(domain).get_dns_records()
    
        if len(dns_records) == 0:
            mcwrite(LM().get(['commands', self.name, 'noRecords']))
            return
        
        print('')

        for dns_record in dns_records:
            for value in dns_record['value']:
                mcwrite(f'{SPACES}&4[&c&l{dns_record["type"]}&4] &f&l{value}')

        # Get the amount of DNS records found 
        records_amount: int = len(dns_records)

        mcwrite(LM().get(['commands', self.name, 'done'])
            .replace('%domain%', domain)
            .replace('%recordsAmount%', str(records_amount)
        ))
