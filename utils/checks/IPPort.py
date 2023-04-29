from utils.checks.Port import check_port
from utils.checks.IP import check_ip


def check_ip_port(ip_port):
    """
    Check if the entered IP and port are valid. (IP:PORT)

    Parameters:
        ip_port (str): IP Address and Port.
    
    Returns:
        bool: Returns true if it is valid.
    """

    if ':' in ip_port:
        ip_port = ip_port.split(':')

        if check_ip(ip_port[0]):
            if check_port(ip_port[1]):
                try:
                    ip_port[2]
                    return False

                except IndexError:
                    return True
                
    return False
