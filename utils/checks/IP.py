#!/usr/bin/python3

import socket


def check_ip(ip_address):
    """ 
    Check if the ip address is valid 
    
    :param ip_address: IP Address
    :return: Boolean value that says if the IP is valid
    """

    try:
        socket.inet_pton(socket.AF_INET, ip_address)
        return True

    except socket.error:
        return False