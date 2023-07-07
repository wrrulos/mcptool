from utils.velocity.start_velocity import start_velocity


def velocity_command(server, mode):
    """
    Starts a velocity proxy that redirects 
    to the specified server.

    Args:
        server (str): Server.
        mode (str): Mode
    """

    start_velocity(server, mode)
