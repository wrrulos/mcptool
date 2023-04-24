from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.mccolor import mcreplace
from utils.managers.Settings import SettingsManager

sm = SettingsManager()
settings = sm.read('settings')


def show_server(ip, motd, version, protocol, connected_players, player_limit, players, bot_output):
    """
    Show server data on screen 

    Parameters:
    ip (str): IP adress
    motd (str): MOTD
    version (str): Server Version
    protocol (str): Server protocol
    connected_players (str): Players connected to the server
    player_limit (str): Limit of players on the server
    bot_output (str): Bot Output
    """

    paint(f'\n     &4[&cI&f&lP&4] &f&l{ip}')
    paint(f'     &4[&cMO&f&lTD&4] &f&l{motd}')
    paint(f'     &4[&cVer&f&lsion&4] &f&l{version}')
    paint(f'     &4[&cProto&f&lcol&4] &f&l{protocol}')
    paint(f'     &4[&cPlay&f&lers&4] &f&l{connected_players}&8&r/&f&l{player_limit}')

    if players is not None and len(players) >= 1:
        paint(f'     &4[&cNam&f&les&4] &f&l{players}')

    if bot_output is not None:
        paint(f'     &4[&cChe&f&lcker&4] &f&l{mcreplace(bot_output)}')


def show_timed_out_server(ip):
    """ 
    Show timed out server on screen 
    
    ip (str): IP Adress
    """

    paint(f'\n     &4[&cI&f&lP&4] &f&l{ip} ({language["timed_out_servers"]["SHOW_SERVER"]}&f&l)')