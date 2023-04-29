def check_domain(server):
    """ 
    Check if the entered server is a domain.
    Otherwise it is an IP address.
    
    Parameters:
        server (str): Minecraft server.

    Returns:
        bool: True if the server is a domain, false if it is an IP address.
    """

    for i in server:
        if i.isdigit() or i == ':' or i == '.':
            continue

        else:
            return True

    return False
