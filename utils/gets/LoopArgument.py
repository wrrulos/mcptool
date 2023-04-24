def get_loop_argument(argument):
    """  
    Returns the scan method. 

    This function is made to simplify the code since the user can enter 
    the method by numbers or by its respective name.

    Parameters:
    loop (str): Loop argument

    Returns:
    bool: Boolean value that checks if it is positive
    """

    if argument == 'y' or argument == 'yes':
        return True

    return False