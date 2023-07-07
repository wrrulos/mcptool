import requests
import socket
import json


def get_ip_ngrok():
    """ 
    Returns the IP address of the ngrok tunnel 
    
    Returns:
        str: Value None or ip address of the ngrok domain
    """

    try:
        r = requests.get('http://localhost:4040/api/tunnels')
        r_unicode = r.content.decode('utf-8')
        r_json = json.loads(r_unicode)
        domain = r_json['tunnels'][0]['public_url']
        domain = domain.replace('tcp://', '')
        domain = domain.split(':')
        ip_address = socket.gethostbyname(str(domain[0]))
        ip_address = f'{ip_address}:{domain[1]}'
        return ip_address

    except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
        return None
