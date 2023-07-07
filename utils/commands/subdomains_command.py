import socket

from utils.color.text_color import paint
from utils.gets.get_spaces import get_spaces
from utils.managers.language_manager import language_manager


def subdomains_command(domain, wordlist, *args):
    """
    Find subdomains for a given domain using a wordlist.
    
    Args:
        domain (str): The target domain to check for subdomains.
        wordlist (str): The path to a text file containing a list of subdomains.
    """

    try:
        subdomains = 0

        with open(wordlist, 'r', encoding='utf8') as f:
            subdomain_list = f.readlines()

        subdomain_list = [subdomain.strip() for subdomain in subdomain_list]
        print('')

        for subdomain in subdomain_list:
            try:
                host = f'{subdomain}.{domain}'
                ip = socket.gethostbyname(host)
                paint(f'{get_spaces()}{language_manager.language["commands"]["subdomains"]["found"].replace("[0]", host).replace("[1]", ip)}')
                subdomains += 1

            except socket.gaierror:
                continue

        if subdomains >= 1:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["subdomains"]["subdomainsFound"].replace("[0]", str(subdomains))}')

        else:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["subdomains"]["subdomainsNotFound"]}')

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return

    except (UnicodeError, PermissionError):
        paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidFile"].replace("[0]", wordlist)}')
        return