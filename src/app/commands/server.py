from src.app.utilities.minecraft.server.get_server import MCServerData
from src.app.utilities.minecraft.server.show_server import ShowMinecraftServer


class Command:
    def __init__(self):
        self.name = 'server'
        self.arguments_length = 1

    def validate_arguments(self, arguments: list) -> bool:
        """
        Method to validate the arguments
        """

        if len(arguments) != self.arguments_length:
            print(f'Invalid number of arguments for {self.name}')
            return False

        return True

    def execute(self, arguments) -> None:
        """
        Method to execute the command
        """

        if not self.validate_arguments(arguments):
            return

        server_data = MCServerData(arguments[0]).get()

        if server_data is None:
            print('Server is offline')
            return

        ShowMinecraftServer().show(server_data=server_data)
