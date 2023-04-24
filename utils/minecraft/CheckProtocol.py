import json


def check_protocol(protocol):
    """
    Check if the protocol entered by the user is 
    compatible with Mineflayer.

    Parameters:
    protocol (str): Protocol

    Returns:
    bool: True if the protocol is compatible, False if it is not.
    """

    with open('utils/minecraft/InvalidProtocols.json', 'r') as f:
        js = json.loads(f.read())

    if protocol in js['INVALID_PROTOCOLS']:
        return False

    return True