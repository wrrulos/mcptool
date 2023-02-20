#!/usr/bin/python3


def check_scan_method(method):
    """ 
    Check if scan method is valid 
    
    :param method: Scan Method
    :return: Boolean value that defines if the method is valid
    """

    methods = ['nmap', 'qubo', 'quboscanner', '0', '1']

    if method in methods:
        return True

    return False