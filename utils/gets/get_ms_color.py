def get_ms_color(ms):
    """
    Returns a Minecraft chat color code based on the provided latency in milliseconds.

    Args:
        ms (int): The latency in milliseconds.

    Returns:
        str: A string representing the Minecraft chat color code.
    """

    if int(ms) <= 100:
        return f'&a{ms}'

    elif int(ms) <= 250:
        return f'&e{ms}'

    else:
        return f'&c{ms}'
