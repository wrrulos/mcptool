#!/usr/bin/python3


def check_iprange(iprange):
    """ 
    Check if the ip range is valid 
    
    :param iprange: IP Range
    :return: Boolean value that tells if the ip range is valid
    """

    try:
        iprange = iprange.split('.')

        if len(iprange) != 4:
            return False
            
        for ip in iprange:
            if not ip == '*':
                if '-' in ip:
                    ip = ip.split('-')

                    if len(ip) != 2:
                        return False

                    for i in ip:
                        if not int(i) in range(0, 256):
                            return False
                    
                else:
                    if not int(ip) >= 0 and not int(ip) < 255:
                        return False
            
        return True

    except IndexError:
        return False

    except ValueError:
        return False

