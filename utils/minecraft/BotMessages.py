def replace_messages(text):
    """
    Replace minecraft characters from messages 
    
    Parameters:
        text (str): Original text
    
    Returns:
        str: Clean text without characters
    """

    messages = {
        'This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details.': '§dForge Server',
        'This server has mods that require Forge to be installed on the client. Contact your server admin for more details.': '§dForge Server',
        'If you wish to use IP forwarding please enable it in your BungeeCord config as well!': '§cVulnerable to Bungee Exploit',
        'multiplayer.disconnect.invalid_public_key_signature': '§cInvalid signature for profile public key',
        'multiplayer.disconnect.banned_ip.reasonwith': '§cYou are IP banned for the following reason: ',
        'multiplayer.disconnect.banned.reasonwith': '§cYou are banned for the following reason: ',
        'multiplayer.disconnect.incompatiblewith': '§cIncompatible versions: ',
        'multiplayer.disconnect.unverified_username': '§6Premium Server',
        'multiplayer.disconnect.not_whitelisted': '§bWhitelist',
        'disconnect.genericReasonwith': '§c',
        'You are not whitelisted on this server!': '§bWhitelist',
        'http//Minecraft.netMinecraft.net': 'http//Minecraft.net',
    }

    for message in messages.items():
        text = text.replace(message[0], message[1])
    
    text = text.replace('\n', '')
    return text
