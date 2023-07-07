from utils.gets.get_player_uuid import player_uuid


def uuid_color(username, uuid):
    """
    Returns whether the user's uuid is premium, 
    non-premium, or modified.

    Args:
        username (str): Username
        uuid (str): UUID

    Returns:
        str: UUID Color
    """

    online_uuid, offline_uuid = player_uuid(username)

    if uuid == online_uuid:
        return '&a'
    
    elif uuid == offline_uuid:
        return '&7'
    
    else:
        return '&5'
    
