import re

from utils.checks.IP import check_ip


def get_ips_from_file(file):
    """"
    Gets the IP addresses from the file to use in the scan command.

    It is recommended to follow the following format in the file:

    127.0.0.1
    127.0.0.2
    127.0.0.3

    Parameters:
    file (str): File

    Returns:
    list: IPs
    """

    ip_list = []

    with open(file, 'r') as f:
        for line in f:
            ips = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
            
            for ip in ips:
                if check_ip(ip):
                    ip_list.append(ip)

    return ip_list
    