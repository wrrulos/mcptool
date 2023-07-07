from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_player_uuid import player_uuid
from utils.gets.get_spaces import get_spaces


def player_command(player):
    """ 
    Gets the premium UUID (if possible) and the 
    non-premium UUID of the specified player.
    
    Args:
        player (str): Minecraft username.
    """

    try:
        online_uuid, offline_uuid = player_uuid(player)

        # If the minecraft user is premium.
        if online_uuid is not None:
            paint(f'\n{get_spaces()}&4[&cUU&f&lID&4] {language_manager.language["commands"]["player"]["onlineUUID"]} {online_uuid}\n{get_spaces()}&4[&cUU&f&lID&4] {language_manager.language["commands"]["player"]["offlineUUID"]} {offline_uuid}')
            
        else:
            paint(f'\n{get_spaces()}&4[&cUU&f&lID&4] {language_manager.language["commands"]["player"]["offlineUUID"]} {offline_uuid}')

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
