import socket


def check_ip(ip_address):
    """ 
    Check if the ip address is valid.
    
    Parameters:
        ip_address (str): IP Address.
    
    Returns
        bool: Returns True if the entered ip is valid.
    """

    try:
        socket.inet_pton(socket.AF_INET, ip_address)
        return True

    except socket.error:
        return False
