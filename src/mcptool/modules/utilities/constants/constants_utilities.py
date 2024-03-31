import sys

from loguru import logger

from ..termux.termux_utilities import TermuxUtilities

 
class ConstantsUtilities:
    @staticmethod
    @logger.catch
    def get_spaces():
        """
        Method to get the number of spaces in the current environment

        Returns:
            int: The number of spaces in the current environment
        """

        return 2 if TermuxUtilities.is_termux() else 4
    
    @staticmethod
    @logger.catch
    def get_os_name():
        """
        Method to get the OS name

        Returns:
            str: The OS name
        """

        if TermuxUtilities.is_termux():
            return 'termux'
        
        if sys.platform.startswith('linux'):
            return 'linux'
        
        if sys.platform.startswith('win'):
            return 'windows'
        
        if sys.platform.startswith('darwin'):
            return 'mac'
        
        return 'unknown'
    
    @staticmethod
    @logger.catch
    def get_prefix():
        """
        Method to get the prefix

        Returns:
            str: The prefix
        """

        return '&f&l[&c&l#&f&l]'


PREFIX = ConstantsUtilities.get_prefix()
SPACES = ConstantsUtilities.get_spaces()
OS_NAME = ConstantsUtilities.get_os_name()