from app.minecraft.server.get_data import MCServerData


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
        
        print(f'{self.name} {arguments}')
        server = MCServerData(arguments[0]).get()
        print(server)