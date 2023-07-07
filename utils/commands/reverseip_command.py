import socket

from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_spaces import get_spaces


def reverseip_command(ip_address):
    """ 
    Get the hostnames that have DNS (A)
    records associated with the specified IP address.
    
    Args:
        ip_address (str): IP Address.
    """

    try:
        domains = socket.gethostbyaddr(ip_address)[0]
        print('')

        if type(domains) == list:
            for domain in domains:
                paint(f'{get_spaces()}{language_manager.language["commands"]["reverseip"]["result"]} &f&l{domain}')

        else:
            paint(f'{get_spaces()}{language_manager.language["commands"]["reverseip"]["result"]} &f&l{domains}')

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return

    except socket.herror:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["reverseip"]["notFound"]}')
