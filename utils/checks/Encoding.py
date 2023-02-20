#!/usr/bin/python3


def check_encoding(file):
    """ 
    Returns the encoding type of the file 
    
    :param file: File
    :return: File encoding mode
    """

    try:
        with open(file, 'r+', encoding='utf8') as f:
            f.read()

        return 'utf8'

    except:
        return 'unicode_escape'