def check_loop_argument(argument):
    """ 
    Check if the loop argument is valid. 
    

    Args:
        argument: Loop argument.

    Returns:
        bool: Returns true if the argument is valid.
    """

    valid_arguments = ['yes', 'y', 'no', 'n']

    if argument in valid_arguments:
        return True

    return False
