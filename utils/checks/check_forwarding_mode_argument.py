def check_forwardingmode_argument(argument):
    """
    Check if the forwarding-mode argument is valid.
    
    Args:
        argument (str): Forwarding-mode argument.

    Returns:
        bool: Returns True if the argument is valid, otherwise False.
    """

    valid_arguments = ['none', 'legacy', 'bungeeguard', 'modern']

    if argument.lower() in valid_arguments:
        return True

    return False
