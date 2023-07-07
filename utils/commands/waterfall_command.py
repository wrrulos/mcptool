from utils.waterfall.start_waterfall import start_waterfall


def waterfall_command(server):
    """
    Starts a waterfall proxy that redirects 
    to the specified server.

    Args:
        server (str): Server.
    """

    start_waterfall(server)
