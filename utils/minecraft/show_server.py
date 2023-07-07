from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.mccolor import mcreplace
from utils.gets.get_ms_color import get_ms_color
from utils.managers.config_manager import config_manager
from utils.gets.get_spaces import get_spaces


def show_server(data, bot_output=False):
    """
    Show server data on screen

    Args:
        data (list): Server data.
        bot_output (bool): Bot Output.
    """

    paint(f'\n{get_spaces()}&4[&cI&f&lP&4] &f&l{data[1]} &7&l(&c&l{data[0]}&7&l)')

    if data[0] == 'Java':
        paint(f'{get_spaces()}&4[&cMO&f&lTD&4] &f&l{data[12]}')
        paint(f'{get_spaces()}&4[&cVer&f&lsion&4] &f&l{data[13]}')

    else:
        paint(f'{get_spaces()}&4[&cMO&f&lTD&4] &f&l{data[10]}')
        paint(f'{get_spaces()}&4[&cVer&f&lsion&4] &f&l{data[11]}')

    paint(f'{get_spaces()}&4[&cProto&f&lcol&4] &f&l{data[4]}')
    paint(f'{get_spaces()}&4[&cPlay&f&lers&4] &f&l{data[5]}&8&r/&f&l{data[6]}')

    if data[0] == 'Java':
        if len(data[10]) >= 1 and data[10] is not None:
            if config_manager.config['showServerMods']:
                paint(f'{get_spaces()}&4[&cMo&f&lds&4] &f&l{data[10]}')

            else:
                paint(f'{get_spaces()}&4[&cMo&f&lds&4] &f&l{data[10]}')

        if data[7] is not None and len(data[7]) >= 1:
            paint(f'{get_spaces()}&4[&cNam&f&les&4] &f&l{data[7]}')

        data[11] = get_ms_color(data[11])

    if data[0] == 'Bedrock':
        if len(data[7]) >= 1 and data[7] is not None:
            paint(f'{get_spaces()}&4[&cMa&f&lp&4] &f&l{data[7]}')

        paint(f'{get_spaces()}&4[&cGame&f&lmode&4] &f&l{data[8]}')
        data[9] = get_ms_color(data[9])

    if bot_output:
        paint(f'{get_spaces()}&4[&cChe&f&lcker&4] &f&l{mcreplace(bot_output)}')

    if data[0] == 'Java':
        paint(f'{get_spaces()}&4[&cPi&lng&4] &f&l{data[11]}ms')

    else:
        paint(f'{get_spaces()}&4[&cPi&lng&4] &f&l{data[9]}ms')


def show_timed_out_server(ip):
    """ 
    Show timed out server on screen 
    
    ip (str): IP Address
    """

    paint(f'\n{get_spaces()}&4[&cI&f&lP&4] &7&l{ip} ({language_manager.language["showTimedOutServer"]}&7&l)')
