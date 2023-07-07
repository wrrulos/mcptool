import socket


def get_ip_address(hostname):
    """
    Retrieves the IP address associated with the given hostname.

    Args:
        hostname (str): The hostname for which to obtain the IP address.

    Returns:
        str: The IP address of the hostname, or None if an error occurs.
    """

    try:
        ip_address = socket.gethostbyname(str(hostname))
        return ip_address

    except socket.error:
        return None
