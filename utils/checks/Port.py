#!/usr/bin/python3


def check_port(port):
    """ 
    Check if the port is valid 
    
    :param port: Port
    :return: Boolean value that tells if the port is valid
    """

    try:
        if int(port) <= 65535:
            return True

        return False

    except ValueError:
        return False