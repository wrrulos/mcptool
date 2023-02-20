#!/usr/bin/python3


def get_bot_argument(argument):
    """  
    Returns the scan method. 

    This function is made to simplify the code since the user can enter 
    the method by numbers or by its respective name.

    :param argument: Bot Argument
    :return: Boolean value that checks if it is positive
    """

    if argument == 'y' or argument == 'yes':
        return True

    return False