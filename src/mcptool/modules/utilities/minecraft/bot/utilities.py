import random

from ...path.mcptool_path import MCPToolPath


class BotUtilities:
    @staticmethod
    def get_bot_username() -> str:
        """
        Method to get the bot username

        Returns:
            str: The bot username
        """

        # Get the path of the MCPTool folder
        path: str = MCPToolPath().get()

        try:
            # Read the bot username from the file
            with open(f'{path}/txt/bot_username.txt', 'r') as file:
                lines = file.readlines()
                return random.choice(lines).strip()

        except FileNotFoundError:
            return 'MCPToolBot'
