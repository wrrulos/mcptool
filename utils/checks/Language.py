#!/usr/bin/python3

valid_languages = ['spanish', 'english']


def check_language(argument):
    """ 
    Check language argument 
    
    :param argument: Loop argument
    :return: Boolean value that tells if the language argument is valid
    """

    if argument in valid_languages:
        return True

    return False