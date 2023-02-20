#!/usr/bin/python3

from utils.color.ColoredCharacters import replace_colors
from mcrcon import MCRcon, MCRconException
from utils.gets.Language import language
from utils.color.TextColor import paint


def rconnect_command(server, password):
    """
    This command connects to the RCON port of a server
    and allows you to enter commands

    :param server: IP address and rcon port of the server
    :param password: Server RCON password
    """

    paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rconnect"]["CONNECTING"]}')
    server = server.split(':')
    mcr = None
    
    try:        
        with MCRcon(server[0], password, int(server[1]), timeout=35) as mcr:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rconnect"]["ESTABLISHED_CONNECTION"]}\n')

            while True:
                paint(f'    {language["script"]["PREFIX"]}{language["commands"]["rconnect"]["COMMAND"]} ', '')
                command = input()

                if command == '.exit':
                    paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rconnect"]["STOPPING"]}')
                    mcr.disconnect()
                    return

                resp = mcr.command(command)
                resp = replace_colors(resp)
                paint(f'\n    {resp}')

    except TimeoutError:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rconnect"]["TIMEOUT"]}')
        return
    
    except ConnectionRefusedError:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rconnect"]["REFUSED_CONNECTION"]}')
        return
    
    except KeyboardInterrupt:
        if mcr is not None:
            mcr.disconnect()

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rconnect"]["STOPPING"]}')
        return

    except MCRconException:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rconnect"]["INVALID_PASSWORD"]}')
        return
    



        
    
