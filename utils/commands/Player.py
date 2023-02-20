#!/usr/bin/python3

from utils.gets.PlayerUUID import player_uuid
from utils.gets.Language import language
from utils.color.TextColor import paint


def player_command(player):
    """ 
    Gets the information from the specified player 
    
    :param player: Player username
    """

    try:
        online_uuid, offline_uuid = player_uuid(player)

        if online_uuid is not None:
            paint(f'\n    [red][[lred]UU[lwhite]ID[red]] {language["commands"]["player"]["ONLINE_UUID"]} {online_uuid}\n    [red][[lred]UU[lwhite]ID[red]] {language["commands"]["player"]["OFFLINE_UUID"]} {offline_uuid}')
            
        else:
            paint(f'\n    [red][[lred]UU[lwhite]ID[red]] {language["commands"]["player"]["OFFLINE_UUID"]} {offline_uuid}')

    except KeyboardInterrupt:
        return