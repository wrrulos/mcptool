import sys

from .termux.termux_utilities import TermuxUtilities


class Utilities:
    @staticmethod
    def get_spaces():
        """
        Method to get the number of spaces in the current environment

        Returns:
            int: The number of spaces in the current environment
        """

        return 2 if TermuxUtilities.is_termux() else 4
    
    @staticmethod
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
