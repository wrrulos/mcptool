from utils.minecraft.ServerData import mcsrvstatus


def get_ip_port(server):
    """ 
    Get only ip and port of the server 
    
    Parameters:
        server (str): Server domain
    
    Returns:
        str: IP and Port or None
    """

    data = mcsrvstatus(server)

    if data is not None:
        return data[0], data[1]

    else:
        return None, None
