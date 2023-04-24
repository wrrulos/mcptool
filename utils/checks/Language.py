import os


def check_language(language):
    """ 
    Check if the entered language is valid.
    
    Parameters:
    language (str): Language.

    Returns: 
    bool: Returns true if the language is valid.
    """

    valid_languages = os.listdir('settings/lang/')
    language += '.json'

    if language in valid_languages:
        return True

    return False