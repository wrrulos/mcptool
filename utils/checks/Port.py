def check_port(port):
    """ 
    Check if the entered port is valid.
    
    Parameters:
    port (str: Ports.
    
    Returns:
    bool: Returns true if the entered port is valid.
    """

    try:
        if int(port) <= 65535:
            return True

        return False

    except ValueError:
        return False