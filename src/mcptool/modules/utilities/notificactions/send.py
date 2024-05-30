from plyer import notification

from ..termux.termux_utilities import TermuxUtilities
from ..path.mcptool_path import MCPToolPath


class SendNotification:
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message

    def send(self) -> None:
        """
        Send a notification to the user with the title and message
        """

        if TermuxUtilities.is_termux():
            return

        notification.notify(
            title=self.title,
            message=self.message,
            app_name='MCPTool',
            app_icon=f'{MCPToolPath().get()}/img/icon.ico',
            timeout=2
        )
