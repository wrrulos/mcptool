from loguru import logger


class ExternalScanner:
    def __init__(self, scanner: str) -> None:
        self.scanner: str = scanner
        self.open_ports: list = []

    @logger.catch
    def scan(self, ip_address: str, port_range: str) -> list:
        """
        Method to scan the ports of the IP address

        Args:
            ip_address (str): The IP address to scan
            port_range (str): The port range to scan

        Returns:
            list: The list of open ports
        """

        if self.scanner == 'nmap':
            self.open_ports = NmapScanner(ip_address=ip_address, port_range=port_range).scan()

        return self.open_ports