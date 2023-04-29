def check_scan_method(method):
    """ 
    Check the scanning method is valid.
    
    Parameters:
        method (str): Scan method

    Returns:
        bool: Returns True if the scan method is valid.
    """

    methods = ['nmap', 'qubo', 'quboscanner', '0', '1']

    if method in methods:
        return True

    return False
