from utils.minecraft.server_data import GetDataFromMinecraftServer


def active_server(ip):
    """
    Check if a Minecraft server is active.

    Args:
        ip (str): The IP address of the Minecraft server.

    Returns:
        bool: True if the server is active, False otherwise.
    """

    server_data = GetDataFromMinecraftServer(server=ip)
    data = server_data.get_information()

    if data is not None:
        # If the server data is not None, it means the server is active and responded to the query.
        return True

    # If the server data is None, it means the server is not active or did not respond.
    return False
