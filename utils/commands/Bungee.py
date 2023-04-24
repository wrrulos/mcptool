from utils.waterfall.StartWaterfall import start_waterfall


def bungee_command(server):
    """
    Starts a waterfall proxy that redirects 
    to the specified server.

    Parameters:
    server (str): Server.
    """

    start_waterfall(server)