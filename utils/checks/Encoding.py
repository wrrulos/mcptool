def check_encoding(file):
    """ 
    Returns the encoding type of the file.
    
    Parameters:
    file (str): File.

    Returns:
    str: File encoding mode.
    """

    try:
        with open(file, 'r+', encoding='utf8') as f:
            f.read()

        return 'utf8'

    except:
        return 'unicode_escape'