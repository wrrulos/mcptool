#!/usr/bin/python3

# This script gets the valid nodes from the host

import socket
import json


def get_host_nodes(hostname):
    """ 
    Get only ip and port of the server 
    
    :param hostname: Hostname
    :return: False or list of server nodes
    """

    valid_nodes = []

    with open(f'utils/hostnames/{hostname}', 'r') as f:
        data = json.loads(f.read())
        domain = data['domain']
        nodes = data['nodes']

    if len(nodes) == 0:
        return False

    for node in nodes:
        try:
            ip = socket.gethostbyname(f'{str(node)}.{str(domain)}')
            valid_nodes.append(ip)

        except (socket.gaierror, socket.timeout):
            pass

    if len(valid_nodes) == 0:
        return False
    
    return valid_nodes

