def check_encoding(file):
    """ 
    Returns the encoding type of the file.
    
    Args:
        file (str): File.

    Returns:
        str: File encoding mode.
    """

    try:
        with open(file, 'r+', encoding='utf8') as f:
            f.read()

        return 'utf8'

    except (UnicodeError, UnicodeDecodeError, UnicodeEncodeError, LookupError):
        return 'unicode_escape'
