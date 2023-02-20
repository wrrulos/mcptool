#!/usr/bin/python3

# This command is responsible for obtaining basic information from a Minecraft server
# server [ip:port/domain]

from utils.minecraftserver.ServerData import mcstatus
from utils.minecraftserver.ShowServer import show_server
from utils.gets.IPAndPort import get_ip_port
from utils.gets.Language import language
from utils.color.TextColor import paint
from utils.checks.Domain import check_domain


def server_command(server):
    """ 
    Gets information about the specified server

    :param server: IP Adress and Port
    """

    try:
        old_server = server

        if check_domain(server):
            ip, port = get_ip_port(server)

            if ip is not None:
                server = f'{ip}:{port}'

        data = mcstatus(server)

        if data is not None:
            show_server(server, data[0], data[1], data[2], data[3], data[4], data[5], None)

        else:
            if check_domain(server):
                data = mcstatus(old_server)

                if data is not None:
                    show_server(server, data[0], data[1], data[2], data[3], data[4], data[5], None)
                    return

            paint(f'\n    {language["commands"]["ERROR"]}{language["commands"]["server"]["INVALID_SERVER"]}')

    except KeyboardInterrupt:
        return




