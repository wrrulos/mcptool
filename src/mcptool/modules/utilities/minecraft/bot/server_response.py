import subprocess

from subprocess import CompletedProcess
from loguru import logger

from ...path.mcptool_path import MCPToolPath


class BotServerResponse:
    def __init__(self, ip_address: str, port: int, version: str) -> None:
        self.ip_address = ip_address
        self.port = port
        self.version = version
        self._response = None

    @logger.catch
    def get_response(self) -> str:
        """
        Method to get the response

        Returns:
            str: The response from the server
        """

        self._send_command()
        return self._response

    @logger.catch
    def _send_command(self):
        """
        Method to send the command to the server
        """

        response: CompletedProcess = subprocess.run(self._get_command(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if there is an error
        if response.stderr:
            error_message = response.stderr.decode('utf-8')
            logger.warning(f'Error sending command: {error_message}')
            self._response = '&cError (Check the logs)'
            return

        self._response = response.stdout.decode('utf-8')

    @logger.catch
    def _get_command(self) -> str:
        """
        Method to get the command to send to the server

        Returns:
            str: The command to send to the server
        """
        
        path: str = MCPToolPath().get()
        return f'cd {path} && node scripts/server_response.mjs {self.ip_address} {self.port} MCPToolBot {self.version}'
