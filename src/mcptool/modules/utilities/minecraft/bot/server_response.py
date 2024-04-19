import subprocess

from subprocess import CompletedProcess
from loguru import logger

from ...path.mcptool_path import MCPToolPath
from ..text.text_utilities import TextUtilities
from ...constants import OS_NAME
from .utilities import BotUtilities


class BotServerResponse:
    def __init__(self, ip_address: str, port: int, version: str, username: str = BotUtilities.get_bot_username()) -> None:
        self.ip_address = ip_address
        self.port = port
        self.version = version
        self.username = username
        self._response = None

    @logger.catch
    def get_response(self) -> str:
        """
        Method to get the response

        Returns:
            str: The response from the server
        """

        # Send the command
        self._send_command()

        # Get the text from the json if it is a json
        self._response = TextUtilities.get_text_from_json(self._response)

        # Remove new lines and quotes and return the response
        self._response = self._response.replace('\n', '').replace('"', '').replace("'", '')
        return self._response

    @logger.catch
    def _send_command(self) -> None:
        """
        Method to send the command to the server
        """

        response: CompletedProcess = subprocess.run(self._get_command(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if there is an error
        if response.stderr:
            error_message = response.stderr.decode('utf-8')
            logger.warning(f'Error sending command: {self._get_command()} -> {error_message}')
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
        command: str = f'cd {path} && node scripts/server_response.mjs {self.ip_address} {self.port} {self.username} {self.version}'

        if OS_NAME == 'windows':
            command = f'C: && {command}'
        
        return command
