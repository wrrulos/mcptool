from datetime import datetime


def get_scan_file():
    """  
    Returns the scan file name.

    It simply returns a variable with the name 
    that will be used to store the scan data.

    Returns:
    str: Scan file name
    """

    date = datetime.now()
    time = f'{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}'
    scan_file = f'temp_scan_{time}.txt'
    return scan_file
