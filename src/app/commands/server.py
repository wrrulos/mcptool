class Command:
    def __init__(self):
        self.name = 'server'
        self.arguments_length = 1

    def validate_arguments(self, arguments):
        """
        Method to validate the arguments
        """

        if len(arguments) != self.arguments_length:
            print(f'Invalid number of arguments for {self.name}')
            return False
        
        return True

    def execute(self, arguments):
        """
        Method to execute the command
        """

        if not self.validate_arguments(arguments):
            return
        
        print(f'{self.name} {arguments}')