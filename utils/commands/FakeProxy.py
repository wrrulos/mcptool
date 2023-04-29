from utils.velocity.StartVelocity import start_velocity


def fakeproxy_command(server, mode):
    """
    Starts a waterfall proxy that redirects 
    to the specified server and captures 
    commands entered by users.

    Parameters:
        server (str): Server.
    """

    start_velocity(server, mode, fakeproxy=True)
