# Module created for my tool MCPTool @wrrulos

from colorama import Fore, init

init()

# COLORS

red = Fore.RED
lred = Fore.LIGHTRED_EX
black = Fore.BLACK
lblack = Fore.LIGHTBLACK_EX
white = Fore.WHITE
lwhite = Fore.LIGHTWHITE_EX
green = Fore.GREEN
lgreen = Fore.LIGHTGREEN_EX
cyan = Fore.CYAN
lcyan = Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lmagenta = Fore.LIGHTMAGENTA_EX
yellow = Fore.YELLOW
lyellow = Fore.LIGHTYELLOW_EX
blue = Fore.BLUE
lblue = Fore.LIGHTBLUE_EX
reset = Fore.RESET


def mc_replace_text_json(text):
    """ Replace the text """
    if '"extra"' in text:
        text = text.replace('"extra"', "")

    if '"obfuscated"' in text:
        text = text.replace('"obfuscated"', "")

    if '"strikethrough"' in text:
        text = text.replace('"strikethrough"', "")

    if '"strikethrough"' in text:
        text = text.replace('"strikethrough"', "")

    if '"underlined"' in text:
        text = text.replace('"underlined"', "")

    if '"italic"' in text:
        text = text.replace('"italic"', "")

    if '"bold"' in text:
        text = text.replace('"bold"', "")

    if '"text"' in text:
        text = text.replace('"text"', "")

    if '"color"' in text:
        text = text.replace('"color"', "")

    if "false," in text:
        text = text.replace("false,", "")

    if "true," in text:
        text = text.replace("true,", "")

    if "{" in text:
        text = text.replace("{", "")

    if "}" in text:
        text = text.replace("}", "")

    if "[" in text:
        text = text.replace("[", "")

    if "]" in text:
        text = text.replace("]", "")

    if ":" in text:
        text = text.replace(":", "")

    if "]," in text:
        text = text.replace("],", "")

    if "text:" in text:
        text = text.replace("text:", "§f")

    if '{"text":' in text:
        text = text.replace('{"text":', "")

    if '"translate"' in text:
        text = text.replace('"translate"', "")

    # if '"dark_red"' in text:

    if '"red"' in text:
        text = text.replace('"red"', "{}".format(red))

    if '"' in text:
        text = text.replace('"', "")

    if "," in text:
        text = text.replace(",", "")

    if "translatemultiplayer.disconnect.unverified_username" in text:
        text = text.replace("translatemultiplayer.disconnect.unverified_username", "§6Premium Server")

    if "translatemultiplayer.disconnect.not_whitelisted" in text:
        text = text.replace('translatemultiplayer.disconnect.not_whitelisted', "§bWhitelist")

    if "translatemultiplayer.disconnect.banned.reasonwith" in text:
        text = text.replace("translatemultiplayer.disconnect.banned.reasonwith", "§cBanned: §f")

    if "translatemultiplayer.disconnect.banned_ip.reasonwith" in text:
        text = text.replace("translatemultiplayer.disconnect.banned_ip.reasonwith", "§cIP Banned: §f")

    if "Not authenticated with clickEventactionopen_urlvaluehttp//Minecraft.netMinecraft.net" in text:
        text = text.replace("Not authenticated with clickEventactionopen_urlvaluehttp//Minecraft.netMinecraft.net", "§eServer premium or bot name is premium and server is semi premium")

    if "You are not whitelisted on this server!" in text:
        text = text.replace("You are not whitelisted on this server!", "§bWhitelist")

    if "multiplayer.disconnect.not_whitelisted" in text:
        text = text.replace("multiplayer.disconnect.not_whitelisted", "§bWhitelist")

    if "This server has mods that require Forge to be installed on the client. Contact your server admin for more details." in text:
        text = text.replace("This server has mods that require Forge to be installed on the client. Contact your server admin for more details.", "§5Forge Server")

    if "This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details." in text:
        text = text.replace("This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details.", "§5Forge Server")

    if "multiplayer.disconnect.unverified_username" in text:
        text = text.replace("multiplayer.disconnect.unverified_username", "§6Premium Server")

    return text


def mc_replace_text_mccolors(text):
    if "§0" in text:
        text = text.replace("§0", "{}".format(lblack))

    if "§1" in text:
        text = text.replace("§1", "{}".format(blue))

    if "§2" in text:
        text = text.replace("§2", "{}".format(lgreen))

    if "§3" in text:
        text = text.replace("§3", "{}".format(cyan))

    if "§4" in text:
        text = text.replace("§4", "{}".format(red))

    if "§5" in text:
        text = text.replace("§5", "{}".format(magenta))

    if "§6" in text:
        text = text.replace("§6", "{}".format(yellow))

    if "§7" in text:
        text = text.replace("§7", "{}".format(lblack))

    if "§8" in text:
        text = text.replace("§8", "{}".format(lblack))

    if "§9" in text:
        text = text.replace("§9", "{}".format(lblue))

    if "§a" in text:
        text = text.replace("§a", "{}".format(lgreen))

    if "§b" in text:
        text = text.replace("§b", "{}".format(lcyan))

    if "§c" in text:
        text = text.replace("§c", "{}".format(lred))

    if "§d" in text:
        text = text.replace("§d", "{}".format(lmagenta))

    if "§e" in text:
        text = text.replace("§e", "{}".format(lyellow))

    if "§f" in text:
        text = text.replace("§f", "{}".format(white))

    if "§k" in text or "§l" in text or "§m" in text or "§n" in text or "§o" in text or "§r" in text:
        text = text.replace("§k", "").replace("§l", "").replace("§m", "").replace("§n", "").replace("§o", "").replace("§r", "")

    if "§A" in text:
        text = text.replace("§A", "{}".format(lgreen))

    if "§B" in text:
        text = text.replace("§B", "{}".format(lcyan))

    if "§C" in text:
        text = text.replace("§C", "{}".format(lred))

    if "§D" in text:
        text = text.replace("§D", "{}".format(lmagenta))

    if "§E" in text:
        text = text.replace("§E", "{}".format(lyellow))

    if "§F" in text:
        text = text.replace("§F", "{}".format(white))

    if "§K" in text or "§L" in text or "§M" in text or "§N" in text or "§O" in text or "§R" in text:
        text = text.replace("§K", "").replace("§L", "").replace("§M", "").replace("§N", "").replace("§O", "").replace("§R", "")

    if "\n" in text:
        text = text.replace("\n", "")

    return text
