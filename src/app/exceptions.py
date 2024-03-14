class EmptyCommandsFolderError(Exception):
    """
    Exception for when the commands folder is empty
    """

    def __init__(self, message="The commands folder is empty"):
        self.message = message
        super().__init__(self.message)
