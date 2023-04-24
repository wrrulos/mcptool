from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.gets.PlayerUUID import player_uuid


def player_command(player):
    """ 
    Gets the premium UUID (if possible) and the 
    non-premium UUID of the specified player.
    
    Parameters:
    player (str): Minecraft username.
    """

    try:
        online_uuid, offline_uuid = player_uuid(player)

        # If the minecraft user is premium.
        if online_uuid is not None:
            paint(f'\n    &4[&cUU&f&lID&4] {language["commands"]["player"]["ONLINE_UUID"]} {online_uuid}\n    &4[&cUU&f&lID&4] {language["commands"]["player"]["OFFLINE_UUID"]} {offline_uuid}')
            
        else:
            paint(f'\n    &4[&cUU&f&lID&4] {language["commands"]["player"]["OFFLINE_UUID"]} {offline_uuid}')

    except KeyboardInterrupt:
        return