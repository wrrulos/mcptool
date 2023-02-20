#!/usr/bin/python3

from utils.checks.Port import check_port


def check_port_range(portrange):
    """ 
    Check if the port range is valid 
    
    :param portrange: Port Range
    :return: Boolean value that tells if the port range is valid
    """

    if "," in portrange:
        portrange = portrange.split(',')

        for ports in portrange:
            if '-' in ports:
                ports = ports.split('-')

                if not check_port(ports[0]):
                    return False

                if not check_port(ports[1]):
                    return False

                if int(ports[0]) > int(ports[1]):
                    return False

            else:
                if not check_port(ports):
                    return False

        return True

    else:
        portrange = portrange.split('-')
        
        if check_port(portrange[0]):
            if check_port(portrange[1]):
                if int(portrange[0]) < int(portrange[1]):
                    return True

        return False

