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