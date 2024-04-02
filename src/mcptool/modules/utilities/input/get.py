from mccolors import mcwrite, mcreplace


class GetInput:
    def __init__(self, input_message: str, input_type: str) -> None:
        self.input_message: str = input_message
        self.input_type: str = input_type

    def get_input(self) -> tuple:
        """
        Method to get the user input and validate it

        Returns:
            tuple: The user input and a boolean value
        """

        while True:
            try:
                user_input: str = input(mcreplace(self.input_message))

                if self.input_type == 'string':
                    return (user_input, True)
                
                if self.input_type == 'integer':
                    try:
                        return (int(user_input), True)
    
                    except ValueError:
                        mcwrite('Invalid input. Please enter a valid integer.')
                        continue

            except KeyboardInterrupt:
                return (None, False)
