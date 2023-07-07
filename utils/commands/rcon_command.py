from mcrcon import MCRcon, MCRconException
from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.mccolor import mcreplace
from utils.gets.get_spaces import get_spaces


def rcon_command(server, password):
    """
    Connect to a server using RCON.

    Args:
        server (str): IP address and RCON port of the server
        password (str): Server RCON password
    """

    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rcon"]["connecting"]}')
    server = server.split(':')
    mcr = None
    
    try:        
        with MCRcon(server[0], password, int(server[1]), timeout=35) as mcr:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rcon"]["establishedConnection"]}\n')

            while True:
                paint(f'{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rcon"]["command"]} ', '')
                command = input()

                if command == '.exit':
                    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rcon"]["stopping"]}')
                    mcr.disconnect()
                    return

                resp = mcr.command(command)
                resp = mcreplace(resp)
                paint(f'\n{get_spaces()}{resp}')

    except TimeoutError:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rcon"]["timeout"]}')
        return
    
    except ConnectionRefusedError:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rcon"]["refusedConnection"]}')
        return
    
    except KeyboardInterrupt:
        if mcr is not None:
            mcr.disconnect()

        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return

    except MCRconException:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["invalidArguments"]["invalidRconPassword"]}')
        return
