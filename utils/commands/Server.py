from utils.checks.Domain import check_domain
from utils.color.TextColor import paint
from utils.gets.IPAndPort import get_ip_port
from utils.gets.Language import language
from utils.minecraft.ServerData import mcstatus
from utils.minecraft.ShowServer import show_server


def server_command(server, *args):
    """ 
    Gets information about the specified Minecraft 
    server and displays it on the screen.

    Parameters:
        server (str): The IP address or domain of the server.
    """

    try:
        old_server = server

        # If a domain is entered, the ip and port are obtained via the mcsrvstatus api.
        if check_domain(server):
            ip, port = get_ip_port(server)

            if ip is not None:
                server = f'{ip}:{port}'

        data = mcstatus(server)

        if data is not None:
            show_server(server, data[0], data[1], data[2], data[3], data[4], data[5], None)
            return

        elif server != old_server:
            if check_domain(old_server):
                data = mcstatus(old_server)

                if data is not None:
                    show_server(server, data[0], data[1], data[2], data[3], data[4], data[5], None)
                    return

        paint(f'\n    {language["commands"]["ERROR"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')

    except KeyboardInterrupt:
        return
