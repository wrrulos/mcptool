#!/usr/bin/python3

valid_arguments = ['yes', 'y', 'no', 'n']


def check_loop_argument(argument):
    """ 
    Check loop argument 
    
    :param argument: Loop argument
    :return: Boolean value that tells if the loop argument is valid
    """

    if argument in valid_arguments:
        return True

    return False