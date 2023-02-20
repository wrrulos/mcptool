#!/usr/bin/python3

from utils.managers.Settings import SettingsManager
from utils.gets.Language import language
from utils.color.TextColor import paint

sm = SettingsManager()
settings = sm.read('settings')


def show_server(ip, motd, version, protocol, connected_players, player_limit, players, bot_output):
    """ 
    Show server data on screen 

    :param ip: IP adress
    :param motd: MOTD
    :param version: Server Version
    :param protocol: Server protocol
    :param connected_players: Players connected to the server
    :param player_limit: Limit of players on the server
    :param bot_output: Bot Output
    """

    if settings['SERVER_DISPLAY_MODE'] == '0':
        paint(f'\n     [red][[lred]I[lwhite]P[red]] [lwhite]{ip}')
        paint(f'     [red][[lred]MO[lwhite]TD[red]] [lwhite]{motd}')
        paint(f'     [red][[lred]Ver[lwhite]sion[red]] [lwhite]{version}')
        paint(f'     [red][[lred]Proto[lwhite]col[red]] [lwhite]{protocol}')
        paint(f'     [red][[lred]Play[lwhite]ers[red]] [lwhite]{connected_players}[lblack]/[lwhite]{player_limit}')

        if players is not None and len(players) >= 1:
            paint(f'     [red][[lred]Nam[lwhite]es[red]] [lwhite]{players}')

        if bot_output is not None:
            paint(f'     [red][[lred]Che[lwhite]cker[red]] [lwhite]{bot_output}')

    elif settings['SERVER_DISPLAY_MODE'] == '1':
        paint(f'\n     [red]([lred]{ip}[red])([lgreen]{connected_players}[lblack]/[lgreen]{player_limit}[red])([lcyan]{version} {protocol}[red])([reset]{motd}[red])', end='')

    else:
        paint(language['server_display_mode']['ERROR'])


def show_timed_out_server(ip):
    """ 
    Show timed out server on screen 
    
    :param ip: IP Adress
    """

    if settings['SERVER_DISPLAY_MODE'] == '0':
        paint(f'\n     [red][[lred]I[lwhite]P[red]] [lwhite]{ip} ({language["timed_out_servers"]["SHOW_SERVER"]}[lwhite])')