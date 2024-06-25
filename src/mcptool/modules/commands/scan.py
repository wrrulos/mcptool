from typing import Union
from mccolors import mcwrite
from loguru import logger

from ..utilities.commands.validate import ValidateArgument
from ..utilities.managers.language_utils import LanguageUtils as LM
from ..utilities.scanner.py_scanner import PyScanner
from ..utilities.scanner.external_scanner import ExternalScanner
from ..utilities.scanner.utilities import ScannerUtilities
from ..utilities.minecraft.nbt.server_dat import ServersDAT
from ..utilities.input.get import GetInput


class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'scan'
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

        if not ValidateArgument.is_scan_method(arguments[2]):
            mcwrite(LM.get('errors.invalidScanMethod'))
            return False

        # Validate the IP address and port range if the method is Python scanner
        if arguments[2] == 'py':
            if not ValidateArgument.is_ip_address(arguments[0]):
                mcwrite(LM.get('errors.invalidIpFormat'))
                return False

            if not ValidateArgument.is_port_range_py_method(arguments[1]):
                mcwrite(LM.get('errors.invalidPortRange'))
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

        # Scan the IP address
        mcwrite(LM.get(f'commands.{self.name}.scanning')
                .replace('%ip%', arguments[0])
                .replace('%portRange%', arguments[1])
                .replace('%method%', arguments[2]))

        # Scan the IP address using the Python scanner
        if arguments[2] == 'py':
            output: Union[dict, None] = PyScanner(ip_address=arguments[0], port_range=arguments[1]).scan()

        else:
            if arguments[2] == 'nmap':
                if not ScannerUtilities.nmap_installed():
                    mcwrite(LM.get('errors.nmapNotInstalled'))
                    return

            if arguments[2] == 'masscan':
                if not ScannerUtilities.masscan_installed():
                    mcwrite(LM.get('errors.masscanNotInstalled'))
                    return

            output: Union[dict, None] = ExternalScanner(target=arguments[0], port_range=arguments[1], scanner=arguments[2]).scan()

        # If there are errors
        if output is None:
            return

        # If there are no open ports
        if output['open_ports']['count'] == 0:
            mcwrite(LM.get(f'commands.{self.name}.noOpenPorts'))
            return

        add_servers: bool = GetInput(LM.get(f'commands.addServersFoundToMinecraft'), 'boolean').get_input()

        if add_servers[0]:
            add_vulnerable_servers_only: bool = GetInput(LM.get(f'commands.addBungeeExploitVulnerableServersOnly'), 'boolean').get_input()

            ServersDAT().add_servers_dat_file(servers=output['open_ports']['bungeeExploitVulnerable'], vulnerables=True)

            if not add_vulnerable_servers_only[0]:
                ServersDAT().add_servers_dat_file(servers=output['open_ports']['minecraft'])

        mcwrite(LM.get(f'commands.{self.name}.openPorts').replace('%openPorts%', str(output['open_ports']['count'])))
