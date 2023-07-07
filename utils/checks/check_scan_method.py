def check_scan_method(method):
    """ 
    Check the scanning method is valid.
    
    Args:
        method (str): Scan method

    Returns:
        bool: Returns True if the scan method is valid.
    """

    methods = ['nmap', 'old_qubo', 'old_quboscanner', 'masscan', '0', '1', '2']

    if method in methods:
        return True

    return False
