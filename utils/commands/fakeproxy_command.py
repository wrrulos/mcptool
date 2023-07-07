from utils.velocity.start_velocity import start_velocity


def fakeproxy_command(server, mode):
    """
    Starts a waterfall proxy that redirects 
    to the specified server and captures 
    commands entered by users.

    Args:
        server (str): Server.
        mode (str): Forwarding mode.
    """

    start_velocity(server, mode, fakeproxy=True)
