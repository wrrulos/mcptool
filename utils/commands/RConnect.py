from mcrcon import MCRcon, MCRconException
from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.mccolor import mcreplace


def rconnect_command(server, password):
    """
    Connect to a server using RCON.

    Parameters:
    server (str): IP address and RCON port of the server
    password (str): Server RCON password
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
                resp = mcreplace(resp)
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

        paint(f'\n\n    {language["script"]["PREFIX"]}{language["commands"]["rconnect"]["STOPPING"]}')
        return

    except MCRconException:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_RCON_PASSWORD"]}')
        return