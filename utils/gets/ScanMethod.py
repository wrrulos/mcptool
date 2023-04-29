def get_scan_method(method):
    """  
    Returns the scan method. 

    This function is made to simplify the code since the user can enter 
    the method by numbers or by its respective name.

    Parameters:
        method (str): Scan method
    
    Returns:
        str: Scan method
    """

    if method == '0' or method == 'nmap':
        return 'nmap'

    if method == '1' or method == 'qubo' or method == 'quboscanner':
        return 'quboscanner'

    #if method == '2' or method == 'masscan':
    #    return 'masscan'
