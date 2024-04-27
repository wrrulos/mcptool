import subprocess

from loguru import logger


class ScannerUtilities:
    @logger.catch
    @staticmethod
    def nmap_installed() -> bool:
        """
        Check if Nmap is installed.

        Returns:
            bool: True if Nmap is installed, False otherwise.
        """

        return subprocess.call(f'nmap --version >nul 2>&1', shell=True) == 0

    @logger.catch
    @staticmethod
    def masscan_installed() -> bool:
        """
        Check if Masscan is installed.

        Returns:
            bool: True if Masscan is installed, False otherwise.
        """

        return subprocess.call(f'masscan --version >nul 2>&1', shell=True) == 0