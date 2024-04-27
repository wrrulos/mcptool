from typing import Union
from mccolors import mcwrite
from loguru import logger

from ..utilities.commands.validate import ValidateArgument
from ..utilities.managers.language_manager import LanguageManager as LM
from ..utilities.input.get import GetInput
from ..utilities.minecraft.proxy.start import StartProxy

class Command:
    @logger.catch
    def __init__(self):
        self.name: str = 'proxy'
        self.arguments: list = [i for i in LM().get(['commands', self.name, 'arguments'])]
        self.target: str = ''
        self.proxy: str = ''
        self.velocity_forwading_mode: tuple = ('', False)

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
        
        if not ValidateArgument.is_ip_and_port(arguments[0]):
            mcwrite(LM().get(['errors', 'invalidIpFormat']))
            return False
        
        if not ValidateArgument.is_proxy_type(arguments[1]):
            mcwrite(LM().get(['errors', 'invalidProxyType']))
            return False
        
        self.target = arguments[0]
        self.proxy = arguments[1]
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
        
        if self.proxy == 'velocity':
            self.velocity_forwading_mode = GetInput(
                input_message=LM().get(['commands', self.name, 'velocityForwardingMode']),
                input_type='velocity_forwarding_mode'
            ).get_input()
        
        print(self.target, self.proxy, self.velocity_forwading_mode, self.velocity_forwading_mode[0])
        StartProxy(target=self.target, proxy=self.proxy, velocity_forwarding_mode=self.velocity_forwading_mode[0]).setup()