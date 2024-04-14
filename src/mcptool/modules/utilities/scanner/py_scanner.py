import threading
import socket

from loguru import logger
from typing import Union
from mccolors import mcwrite

from ..minecraft.server.get_server import BedrockServerData, JavaServerData, MCServerData
from ..minecraft.server.show_server import ShowMinecraftServer
from ..managers.settings_manager import SettingsManager as SM

# Try to get the number of threads for the scanner
try:
    # Semaphore to limit the number of active threads
    thread_semaphore = threading.Semaphore(SM().get(['scannerOptions', 'pyScanner', 'threads']))

except (TypeError, ValueError, KeyError):
    logger.warning('Invalid number of threads for the scanner. Using the default value of 10 threads.')
    thread_semaphore = threading.Semaphore(10)


class PyScanner:
    def __init__(self, ip_address: str, port_range: str) -> None:
        self.ip_address: str = ip_address
        self.port_range: str = port_range
        self.open_ports: list = []
        self.timeout: Union[int, float, None] = SM().get(['scannerOptions', 'pyScanner', 'timeout'])
        self.stopped: bool = False
        self.threads: list = []

        if self.timeout is None:
            logger.warning('Invalid timeout for the scanner. Using the default value of 1 second.')
            self.timeout = 1
    
    @logger.catch
    def scan(self) -> list:
        """
        Method to scan the ports of the IP address

        Returns:
            list: The list of open ports
        """

        # Get the start and end of the port range
        if '-' in self.port_range:
            start, end = self.port_range.split('-')

        else:
            start = end = self.port_range

        logger.info(f'Scanning {self.ip_address} from port {start} to port {end} (Python Scanner)')
        
        # Scan the ports of the IP address
        for port in range(int(start), int(end) + 1):
            if self.stopped:  # Check if the user wants to stop the scan
                break

            # Acquire the semaphore before starting a thread
            thread_semaphore.acquire()
            thread = threading.Thread(target=self._scan_port, args=(port,))

            # Add the thread to the list of threads
            self.threads.append(thread)
            # Start the thread
            thread.start()

        # Wait for all threads to finish
        for thread in self.threads:
            thread.join()

        return self.open_ports
    
    @logger.catch
    def _scan_port(self, port: int) -> None:
        """
        Method to scan a port of the IP address

        Args:
            port (int): The port to scan
        """
        
        try:
            # Try to connect to the port
            sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result: int = sock.connect_ex((self.ip_address, port))

            # If the result is 0, the port is open
            if result == 0:
                # Check if the port is a Minecraft server
                server_data: Union[JavaServerData, BedrockServerData, None] = MCServerData(f'{self.ip_address}:{port}').get()

                if server_data is not None:
                    ShowMinecraftServer.show(server_data)

                else:
                    pass
                    # mcwrite(f'&aPort {port} is open')

                self.open_ports.append(port)

            sock.close()

        except KeyboardInterrupt:
            self.stopped = True

        except Exception as e:
            logger.error(f"Error scanning port {self.ip_address}:{port} -> {str(e)}")

        finally:
            # Release the semaphore after scanning the port
            thread_semaphore.release()
