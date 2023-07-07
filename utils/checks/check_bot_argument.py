def check_bot_argument(argument):
    """ 
    Check if the bot argument is valid.
    
    Args:
        argument (str): Bot argument.

    Returns:
        bool: Returns True if the argument is valid, otherwise False.
    """

    valid_arguments = ['yes', 'y', 'no', 'n']

    if argument in valid_arguments:
        return True

    return False
