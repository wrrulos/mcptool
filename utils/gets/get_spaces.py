from utils.checks.check_termux import check_termux


def get_spaces():
    """
    This function returns the appropriate spacing based on the execution environment.

    If the execution environment is Termux, a single space is returned.
    Otherwise, four spaces are returned.

    Returns:
        spaces (str): The appropriate spacing based on the execution environment.
    """
    
    if check_termux():
        # Set the spacing to a single space for Termux
        spaces = '  '

    else:
        # Set the spacing to four spaces for other environments
        spaces = '    '

    return spaces
