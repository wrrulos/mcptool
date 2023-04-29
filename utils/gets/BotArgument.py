def get_bot_argument(argument):
    """  
    Returns the scan method. 

    This function is made to simplify the code since the user can enter 
    the method by numbers or by its respective name.

    Parameters:
        argument: Bot argument

    Returns:
        bool: Returns true if a bot should be sent.
    """

    if argument == 'y' or argument == 'yes':
        return True

    return False
